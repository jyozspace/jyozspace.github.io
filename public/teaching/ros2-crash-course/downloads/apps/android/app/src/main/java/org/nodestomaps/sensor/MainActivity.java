package org.nodestomaps.sensor;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.graphics.*;
import android.hardware.*;
import android.os.*;
import android.text.InputType;
import android.view.*;
import android.widget.*;
import org.json.*;
import java.util.*;

/** Foreground-only sensor sender. No recording, analytics, account or persistent pairing data. */
public final class MainActivity extends Activity implements SensorEventListener {
    private EditText address,token,pin;
    private TextView status,metrics,capabilities;
    private ImageView preview;
    private Button start,stop;
    private volatile HandlerThread worker;
    private Handler handler;
    private SensorManager sensors;
    private CameraFeed camera;
    private SensorSocket socket;
    private volatile boolean running,clockReady;
    private volatile int epoch;
    private int syncIndex;
    private double sentAt,bestRtt=Double.POSITIVE_INFINITY,bestOffset;
    private final Map<Integer,Long> lastSensor=new HashMap<>();
    private long images,accels,gyros,dropped,imageSeq,accelSeq,gyroSeq;

    public void onCreate(Bundle state) {
        super.onCreate(state);
        sensors=(SensorManager)getSystemService(SENSOR_SERVICE);
        ScrollView scroll=new ScrollView(this);scroll.setFitsSystemWindows(true);LinearLayout content=new LinearLayout(this);content.setOrientation(LinearLayout.VERTICAL);content.setPadding(28,30,28,30);content.setBackgroundColor(Color.rgb(247,245,236));scroll.addView(content);setContentView(scroll);
        label(content,"NODES TO MAPS / ANDROID SENSOR KIT",14);
        label(content,"Your phone.\nA robotics sensor.",30);
        label(content,"Pair with your own laptop. Camera and sensor data travel only to that endpoint.",16);
        address=field(content,"Secure receiver address","wss://LAPTOP:8443/ws/android",false);
        token=field(content,"Session token printed on the laptop","Pairing token",true);
        pin=field(content,"Server certificate SHA-256 printed on the laptop","64 hexadecimal digits",false);
        label(content,"USB: wss://127.0.0.1:8443/ws/android after adb reverse. Wi-Fi: use the laptop’s address on your phone hotspot.",14);
        start=new Button(this);start.setText("Start camera + sensors");content.addView(start);start.setOnClickListener(v->begin());
        stop=new Button(this);stop.setText("Stop & release sensors");stop.setEnabled(false);content.addView(stop);stop.setOnClickListener(v->end("Stopped. Camera and sensors released."));
        status=label(content,"Not connected. Sensors are inactive.",16);
        capabilities=label(content,"Camera mode and timestamp source appear after Start.",14);
        preview=new ImageView(this);preview.setScaleType(ImageView.ScaleType.FIT_CENTER);content.addView(preview,new LinearLayout.LayoutParams(-1,320));
        metrics=label(content,"Images 0 · Accel 0 · Gyro 0 · Skipped 0",16);
        label(content,"10 fps image send target · each motion sensor up to 50 Hz. Preview uses the same unrotated pixels as ROS. Hold one orientation for calibration and mapping. Capture stops when this screen leaves the foreground.",14);
        label(content,"Core project: sparse monocular mapping. Camera–IMU fusion requires measured calibration and a qualified timestamp source.",14);
    }
    private TextView label(LinearLayout parent,String text,int size){TextView v=new TextView(this);v.setText(text);v.setTextSize(size);v.setTextColor(Color.rgb(24,57,46));v.setPadding(0,10,0,14);parent.addView(v);return v;}
    private EditText field(LinearLayout parent,String label,String hint,boolean secret){label(parent,label,15);EditText v=new EditText(this);v.setSingleLine(true);v.setHint(hint);v.setTextSize(15);v.setInputType(secret?InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD:InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);v.setSaveEnabled(false);parent.addView(v);return v;}
    private static JSONObject object(Object... pairs) throws JSONException {JSONObject o=new JSONObject();for(int i=0;i<pairs.length;i+=2)o.put((String)pairs[i],pairs[i+1]);return o;}
    private double now(){return SystemClock.elapsedRealtimeNanos()/1e6;}
    private void fail(int session,String reason){runOnUiThread(()->{if(epoch==session&&running)end(reason);});}
    private void showCounts(int session){runOnUiThread(()->{if(epoch==session)metrics.setText("Images "+images+" · Accel "+accels+" · Gyro "+gyros+" · Skipped "+dropped);});}
    private void begin(){
        if(running)return;
        if(checkSelfPermission(Manifest.permission.CAMERA)!=PackageManager.PERMISSION_GRANTED){requestPermissions(new String[]{Manifest.permission.CAMERA},1);status.setText("Grant camera permission, then tap Start.");return;}
        if(token.getText().toString().trim().isEmpty()){status.setText("Enter the session token printed by phone_bridge.");return;}
        int session=++epoch;
        final String pairingToken=token.getText().toString().trim();
        try {
            worker=new HandlerThread("camera-and-motion");worker.start();handler=new Handler(worker.getLooper());
            camera=new CameraFeed(this,handler,new CameraFeed.Listener(){
                public boolean ready(){return running&&epoch==session&&clockReady&&socket!=null&&!socket.congested();}
                public void failed(String reason){fail(session,reason);}
                public void frame(byte[] jpeg,int width,int height,long timeNs){
                    SensorSocket destination=socket;
                    if(epoch!=session || !running || destination==null || !clockReady || destination.congested()){dropped++;return;}
                    try {
                        boolean accepted=destination.sendSensor(object("type","image","seq",imageSeq++,"t_ms",timeNs/1e6,"width",width,"height",height,"jpeg",android.util.Base64.encodeToString(jpeg,android.util.Base64.NO_WRAP)).toString());
                        if(accepted){images++;runOnUiThread(()->{if(epoch==session&&running){Bitmap bitmap=BitmapFactory.decodeByteArray(jpeg,0,jpeg.length);preview.setImageBitmap(bitmap);}});}else dropped++;
                        showCounts(session);
                    }catch(Exception ex){fail(session,"Image packet: "+ex.getMessage());}
                }
            });
            capabilities.setText("Rear camera "+camera.id+" · "+camera.size+" · native unrotated image\nClock: "+(camera.realtime?"REALTIME — camera and IMU share elapsed-realtime base":"UNKNOWN — image callback estimate; camera-only exercise")+"\nFocus: "+camera.focusMode+" · stabilization requested OFF");
            final CameraFeed capture=camera;final Handler sessionHandler=handler;final SensorSocket[] connection=new SensorSocket[1];
            connection[0]=new SensorSocket(address.getText().toString(),pin.getText().toString(),new SensorSocket.Listener(){
                public void opened(){if(epoch!=session||!running)return;try{if(!connection[0].send(object("type","hello","version",2,"client","android-camera2","token",pairingToken,"camera_id",capture.id,"width",capture.size.getWidth(),"height",capture.size.getHeight(),"sensor_orientation",capture.orientation,"camera_clock",capture.realtime?"realtime":"callback_estimate","focus_mode",capture.focusMode).toString()))throw new IllegalStateException("Handshake queue full");}catch(Exception ex){fail(session,ex.getMessage());}}
                public void failed(String reason){fail(session,reason);}
                public void text(String text){if(epoch==session&&running)sessionHandler.post(()->receive(session,text));}
            });
            socket=connection[0];
            images=accels=gyros=dropped=imageSeq=accelSeq=gyroSeq=0;lastSensor.clear();syncIndex=0;bestRtt=Double.POSITIVE_INFINITY;clockReady=false;running=true;
            start.setEnabled(false);stop.setEnabled(true);address.setEnabled(false);token.setEnabled(false);pin.setEnabled(false);
            getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);status.setText("Connecting with the pinned server certificate…");socket.connect();
        }catch(Exception ex){end("Setup: "+ex.getMessage());}
    }
    private void receive(int session,String text){
        if(!running||epoch!=session)return;
        try {
            JSONObject message=new JSONObject(text);String type=message.getString("type");
            if(type.equals("ready")){sendSync();}
            else if(type.equals("sync")){
                if(!String.valueOf(syncIndex).equals(message.getString("id")))throw new IllegalStateException("Unexpected clock reply");
                double t1=now(),rtt=t1-sentAt;if(rtt<bestRtt){bestRtt=rtt;bestOffset=message.getDouble("server_ms")-(sentAt+t1)/2;}
                syncIndex++;if(syncIndex<7)sendSync();else if(bestRtt>2000)throw new IllegalStateException("Clock RTT too large. Check the connection.");
                else socket.send(object("type","clock","offset_ms",bestOffset,"rtt_ms",bestRtt).toString());
            } else if(type.equals("clock_ready")){
                clockReady=true;
                Sensor a=sensors.getDefaultSensor(Sensor.TYPE_ACCELEROMETER),g=sensors.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
                boolean hasA=a!=null&&sensors.registerListener(this,a,20_000,handler),hasG=g!=null&&sensors.registerListener(this,g,20_000,handler);
                camera.start();
                runOnUiThread(()->{if(epoch==session&&running)status.setText(String.format(Locale.ROOT,"Streaming · clock RTT %.1f ms · accel %s · gyro %s",bestRtt,hasA?"available":"missing",hasG?"available":"missing"));});
            } else if(type.equals("error"))fail(session,"Receiver: "+message.optString("message"));
        }catch(Exception ex){fail(session,"Protocol: "+ex.getMessage());}
    }
    private void sendSync() throws JSONException {sentAt=now();if(!socket.send(object("type","sync","id",String.valueOf(syncIndex),"t0",sentAt).toString()))throw new IllegalStateException("Sync queue full");}
    public void onSensorChanged(SensorEvent event){
        if(Thread.currentThread()!=worker)return;
        int session=epoch;SensorSocket current=socket;
        if(!running||!clockReady||current==null||current.congested())return;
        int type=event.sensor.getType();if(type!=Sensor.TYPE_ACCELEROMETER&&type!=Sensor.TYPE_GYROSCOPE)return;
        if(SystemClock.elapsedRealtimeNanos()-event.timestamp>250_000_000L){dropped++;return;}
        Long last=lastSensor.get(type);if(last!=null&&event.timestamp-last<20_000_000L)return;
        if(event.values.length<3)return;for(int i=0;i<3;i++)if(Float.isNaN(event.values[i])||Float.isInfinite(event.values[i]))return;
        lastSensor.put(type,event.timestamp);
        try {
            boolean accel=type==Sensor.TYPE_ACCELEROMETER;
            if(current.sendSensor(object("type",accel?"accel":"gyro","seq",accel?accelSeq++:gyroSeq++,"t_ms",event.timestamp/1e6,"values",new JSONArray(new float[]{event.values[0],event.values[1],event.values[2]})).toString())){if(accel)accels++;else gyros++;}else dropped++;
            if((accels+gyros)%25==0)showCounts(session);
        }catch(Exception ex){fail(session,"Motion packet: "+ex.getMessage());}
    }
    public void onAccuracyChanged(Sensor sensor,int accuracy){}
    private void end(String message){
        running=false;clockReady=false;epoch++;
        sensors.unregisterListener(this);
        if(socket!=null){socket.close();socket=null;}if(camera!=null){camera.close();camera=null;}
        if(worker!=null){worker.quitSafely();worker=null;}
        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        if(start!=null){start.setEnabled(true);stop.setEnabled(false);address.setEnabled(true);token.setEnabled(true);pin.setEnabled(true);status.setText(message);preview.setImageDrawable(null);}
    }
    protected void onPause(){end("Paused. Camera and sensors released. Tap Start to reconnect.");super.onPause();}
}
