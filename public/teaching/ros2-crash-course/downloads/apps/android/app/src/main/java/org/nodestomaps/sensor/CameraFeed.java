package org.nodestomaps.sensor;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.*;
import android.hardware.camera2.*;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.media.*;
import android.os.*;
import android.util.Size;
import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.util.*;

/** Fixed camera ID and native, unrotated YUV geometry. Calibration applies to these pixels. */
final class CameraFeed implements AutoCloseable {
    interface Listener { void frame(byte[] jpeg,int width,int height,long timeNs); void failed(String reason); boolean ready(); }
    final String id;
    final Size size;
    final int orientation;
    final boolean realtime;
    final String focusMode;
    private final CameraManager manager;
    private final Handler handler;
    private final Listener listener;
    private final CameraCharacteristics characteristics;
    private ImageReader reader;
    private CameraDevice device;
    private CameraCaptureSession session;
    private volatile boolean closed;
    private long lastFrame;

    CameraFeed(Context context,Handler handler,Listener listener) throws CameraAccessException {
        manager=(CameraManager)context.getSystemService(Context.CAMERA_SERVICE);
        this.handler=handler; this.listener=listener;
        String chosen=null;
        for(String camera:manager.getCameraIdList()) {
            CameraCharacteristics c=manager.getCameraCharacteristics(camera);
            Integer facing=c.get(CameraCharacteristics.LENS_FACING);
            if(facing!=null && facing==CameraCharacteristics.LENS_FACING_BACK) {
                if(chosen==null) chosen=camera;
                Integer clock=c.get(CameraCharacteristics.SENSOR_INFO_TIMESTAMP_SOURCE);
                if(clock!=null && clock==CameraCharacteristics.SENSOR_INFO_TIMESTAMP_SOURCE_REALTIME) {chosen=camera;break;}
            }
        }
        if(chosen==null) throw new IllegalArgumentException("A rear camera is required.");
        id=chosen; characteristics=manager.getCameraCharacteristics(id);
        Integer clock=characteristics.get(CameraCharacteristics.SENSOR_INFO_TIMESTAMP_SOURCE);
        realtime=clock!=null && clock==CameraCharacteristics.SENSOR_INFO_TIMESTAMP_SOURCE_REALTIME;
        Integer angle=characteristics.get(CameraCharacteristics.SENSOR_ORIENTATION); orientation=angle==null?0:angle;
        StreamConfigurationMap map=characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
        Size[] sizes=map==null?null:map.getOutputSizes(ImageFormat.YUV_420_888);
        Size selected=null;
        if(sizes!=null) for(Size s:sizes) if(s.getWidth()<=640 && s.getHeight()<=640 && s.getWidth()%2==0 && s.getHeight()%2==0
                && (selected==null || s.getWidth()*s.getHeight()>selected.getWidth()*selected.getHeight())) selected=s;
        if(selected==null) throw new IllegalArgumentException("Camera has no supported YUV stream with both edges <=640 px.");
        size=selected;
        int[] modes=characteristics.get(CameraCharacteristics.CONTROL_AF_AVAILABLE_MODES);
        focusMode=contains(modes,CaptureRequest.CONTROL_AF_MODE_CONTINUOUS_VIDEO)?"continuous-video":"off/fixed";
    }
    private static boolean contains(int[] values,int v) { if(values!=null)for(int x:values)if(x==v)return true;return false; }

    @SuppressLint("MissingPermission") void start() throws CameraAccessException {
        reader=ImageReader.newInstance(size.getWidth(),size.getHeight(),ImageFormat.YUV_420_888,3);
        reader.setOnImageAvailableListener(source->{
            try(Image image=source.acquireLatestImage()) {
                if(image==null || closed || !listener.ready())return;
                long now=SystemClock.elapsedRealtimeNanos(); if(now-lastFrame<100_000_000L)return;lastFrame=now;
                long stamp=realtime?image.getTimestamp():now;
                byte[] nv21=toNv21(image);
                ByteArrayOutputStream encoded=new ByteArrayOutputStream();
                if(!new YuvImage(nv21,ImageFormat.NV21,size.getWidth(),size.getHeight(),null)
                        .compressToJpeg(new Rect(0,0,size.getWidth(),size.getHeight()),75,encoded)) throw new IllegalStateException("JPEG encoding failed");
                listener.frame(encoded.toByteArray(),size.getWidth(),size.getHeight(),stamp);
            } catch(Exception ex) {if(!closed)listener.failed("Camera conversion: "+ex.getMessage());}
        },handler);
        manager.openCamera(id,new CameraDevice.StateCallback(){
            public void onOpened(CameraDevice camera){
                if(closed){camera.close();return;}device=camera;
                try {
                    camera.createCaptureSession(Collections.singletonList(reader.getSurface()),new CameraCaptureSession.StateCallback(){
                        public void onConfigured(CameraCaptureSession capture){
                            if(closed){capture.close();return;}session=capture;
                            try {
                                CaptureRequest.Builder request=device.createCaptureRequest(CameraDevice.TEMPLATE_RECORD);
                                request.addTarget(reader.getSurface());
                                request.set(CaptureRequest.CONTROL_AF_MODE,focusMode.equals("continuous-video")?CaptureRequest.CONTROL_AF_MODE_CONTINUOUS_VIDEO:CaptureRequest.CONTROL_AF_MODE_OFF);
                                request.set(CaptureRequest.CONTROL_VIDEO_STABILIZATION_MODE,CaptureRequest.CONTROL_VIDEO_STABILIZATION_MODE_OFF);
                                int[] ois=characteristics.get(CameraCharacteristics.LENS_INFO_AVAILABLE_OPTICAL_STABILIZATION);
                                if(ois!=null && ois.length>0)request.set(CaptureRequest.LENS_OPTICAL_STABILIZATION_MODE,CaptureRequest.LENS_OPTICAL_STABILIZATION_MODE_OFF);
                                capture.setRepeatingRequest(request.build(),null,handler);
                            }catch(Exception ex){listener.failed("Camera request: "+ex.getMessage());}
                        }
                        public void onConfigureFailed(CameraCaptureSession capture){listener.failed("Camera capture configuration failed.");}
                    },handler);
                }catch(Exception ex){listener.failed("Camera session: "+ex.getMessage());}
            }
            public void onDisconnected(CameraDevice camera){camera.close();if(!closed)listener.failed("Camera disconnected.");}
            public void onError(CameraDevice camera,int error){camera.close();if(!closed)listener.failed("Camera error "+error);}
        },handler);
    }

    static byte[] toNv21(Image image) {
        int w=image.getWidth(),h=image.getHeight(); byte[] result=new byte[w*h*3/2];
        Image.Plane[] planes=image.getPlanes();
        for(int p=0;p<3;p++) {
            ByteBuffer bytes=planes[p].getBuffer(); int rows=p==0?h:h/2,cols=p==0?w:w/2;
            int rowStride=planes[p].getRowStride(),pixelStride=planes[p].getPixelStride(),base=bytes.position();
            for(int y=0;y<rows;y++)for(int x=0;x<cols;x++) {
                int target=p==0?y*w+x:w*h+y*w+2*x+(p==1?1:0);
                result[target]=bytes.get(base+y*rowStride+x*pixelStride);
            }
        }
        return result;
    }
    public void close(){closed=true;if(session!=null)session.close();if(device!=null)device.close();if(reader!=null)reader.close();}
}
