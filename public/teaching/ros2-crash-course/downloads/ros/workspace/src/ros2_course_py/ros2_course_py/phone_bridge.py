"""Authenticated WSS receiver for the native Android sensor app.

The server factory accepts a test sink; ROS is imported only by main/RosSink.
"""
import argparse
import asyncio
import json
from pathlib import Path
import secrets
import ssl
import threading
import time

from aiohttp import web, WSMsgType
from .phone_protocol import Session


def create_app(sink, token):
    active = {'ws': None}

    async def websocket(request):
        origin = request.headers.get('Origin', '')
        if origin:
            raise web.HTTPForbidden(text='Origin not allowed')
        ws = web.WebSocketResponse(max_msg_size=1_000_000, heartbeat=20, receive_timeout=30)
        await ws.prepare(request)
        claimed = False
        session = Session()
        try:
            hello = await ws.receive_json(timeout=10)
            supplied = hello.get('token') if isinstance(hello, dict) else None
            if (not isinstance(supplied, str) or len(supplied) > 256
                    or hello.get('type') != 'hello' or hello.get('version') != 2
                    or hello.get('client') != 'android-camera2'
                    or not secrets.compare_digest(supplied, token)):
                await ws.close(code=1008, message=b'Invalid pairing')
                return ws
            if active['ws'] is not None:
                await ws.close(code=1008, message=b'Laptop already paired')
                return ws
            active['ws'] = ws
            claimed = True
            sink.session_started()
            metadata = {k: str(hello.get(k, 'unknown'))[:180] for k in
                        ('camera_id', 'width', 'height', 'sensor_orientation', 'camera_clock', 'focus_mode')}
            sink.diagnostic({'client': 'android-camera2', 'capture': metadata,
                             'imu_frame': 'phone_android_device', 'imu_fused': False})
            await ws.send_json({'type': 'ready', 'version': 2})
            window_start, count = time.monotonic(), 0
            async for incoming in ws:
                if incoming.type != WSMsgType.TEXT:
                    if incoming.type in (WSMsgType.CLOSE, WSMsgType.ERROR):
                        break
                    raise ValueError('Only JSON text messages are accepted')
                current = time.monotonic()
                if current - window_start >= 1:
                    window_start, count = current, 0
                count += 1
                if count > 150:
                    raise ValueError('Rate limit exceeded')
                data = json.loads(incoming.data)
                if not isinstance(data, dict):
                    raise ValueError('Expected a JSON object')
                if data.get('type') == 'sync':
                    ident = data.get('id')
                    if not isinstance(ident, str) or len(ident) > 32:
                        raise ValueError('Invalid sync id')
                    await ws.send_json({'type': 'sync', 'id': ident,
                                        'server_ms': sink.now_ns() / 1_000_000})
                elif data.get('type') == 'clock':
                    rtt = session.set_clock(data)
                    sink.diagnostic({'clock_rtt_ms': rtt, 'timestamp_quality':
                                     'android_sensor_events_camera_' + str(hello.get('camera_clock', 'unknown'))[:40]})
                    await ws.send_json({'type': 'clock_ready'})
                else:
                    sink.publish(session.sensor(data, sink.now_ns()))
        except (ValueError, TypeError, KeyError, asyncio.TimeoutError) as exc:
            if not ws.closed:
                await ws.send_json({'type': 'error', 'message': str(exc)[:180]})
                await ws.close(code=1008, message=b'Invalid or timed out sensor session')
        finally:
            if claimed:
                active['ws'] = None
                sink.diagnostic({'connection': 'disconnected'})
        return ws

    app = web.Application(client_max_size=1_000_000)
    app.router.add_get('/ws/android', websocket)

    async def shutdown(_):
        if active['ws'] is not None:
            await active['ws'].close(code=1001, message=b'Receiver stopping')
    app.on_shutdown.append(shutdown)
    return app


class RosSink:
    def __init__(self, node, calibration):
        import cv2
        import numpy as np
        import yaml
        from cv_bridge import CvBridge
        from sensor_msgs.msg import Image, CompressedImage, CameraInfo, Imu
        from std_msgs.msg import String
        from rclpy.qos import qos_profile_sensor_data
        self.node, self.cv2, self.np, self.bridge = node, cv2, np, CvBridge()
        self.types = (CompressedImage, CameraInfo, Imu, String)
        self.image = node.create_publisher(Image, '/phone/camera/image_raw', qos_profile_sensor_data)
        self.compressed = node.create_publisher(CompressedImage, '/phone/camera/image_raw/compressed', qos_profile_sensor_data)
        self.info = node.create_publisher(CameraInfo, '/phone/camera/camera_info', qos_profile_sensor_data)
        self.accel = node.create_publisher(Imu, '/phone/imu/accelerometer', qos_profile_sensor_data)
        self.gyro = node.create_publisher(Imu, '/phone/imu/gyroscope', qos_profile_sensor_data)
        self.diag = node.create_publisher(String, '/phone/diagnostics', 10)
        self.calibration = None
        if calibration:
            self.calibration = yaml.safe_load(Path(calibration).read_text())
            for key, size in [('camera_matrix', 9), ('rectification_matrix', 9), ('projection_matrix', 12)]:
                values = self.calibration[key]['data']
                if len(values) != size or not all(np.isfinite(v) for v in values):
                    raise ValueError('Malformed calibration: ' + key)
            if self.calibration['camera_matrix']['data'][0] <= 0:
                raise ValueError('Calibration focal length must be positive')

    def now_ns(self):
        return self.node.get_clock().now().nanoseconds

    def session_started(self):
        self.diagnostic({'connection': 'paired',
                         'imu_is_calibrated': False, 'camera_is_calibrated': bool(self.calibration)})

    def diagnostic(self, values):
        msg = self.types[3]()
        msg.data = json.dumps(values)
        self.diag.publish(msg)

    @staticmethod
    def stamp(header, ns, frame):
        header.stamp.sec, header.stamp.nanosec = divmod(ns, 1_000_000_000)
        header.frame_id = frame

    def publish(self, sample):
        CompressedImage, CameraInfo, Imu, _ = self.types
        if sample['type'] in ('accel', 'gyro'):
            msg = Imu()
            self.stamp(msg.header, sample['stamp_ns'], 'phone_android_device')
            msg.orientation_covariance[0] = -1.0
            if sample['type'] == 'accel':
                msg.angular_velocity_covariance[0] = -1.0
                msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z = sample['values']
                self.accel.publish(msg)
            else:
                msg.linear_acceleration_covariance[0] = -1.0
                msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z = sample['values']
                self.gyro.publish(msg)
            return
        pixels = self.cv2.imdecode(self.np.frombuffer(sample['jpeg'], self.np.uint8), self.cv2.IMREAD_COLOR)
        if pixels is None or pixels.shape[:2] != (sample['height'], sample['width']):
            raise ValueError('Decoded JPEG dimensions do not match declared dimensions')
        msg = self.bridge.cv2_to_imgmsg(pixels, encoding='bgr8')
        self.stamp(msg.header, sample['stamp_ns'], 'phone_camera_optical_frame')
        info = CameraInfo()
        info.header = msg.header
        info.width, info.height = sample['width'], sample['height']
        info.distortion_model = 'plumb_bob'
        if self.calibration:
            c = self.calibration
            if (c['image_width'], c['image_height']) != (info.width, info.height):
                raise ValueError('Calibration resolution mismatch; restore calibrated phone mode')
            info.distortion_model = c['distortion_model']
            info.d = [float(v) for v in c['distortion_coefficients']['data']]
            info.k = [float(v) for v in c['camera_matrix']['data']]
            info.r = [float(v) for v in c['rectification_matrix']['data']]
            info.p = [float(v) for v in c['projection_matrix']['data']]
        compressed = CompressedImage()
        compressed.header, compressed.format, compressed.data = msg.header, 'jpeg', sample['jpeg']
        self.image.publish(msg)
        self.compressed.publish(compressed)
        self.info.publish(info)


def main(args=None):
    import rclpy
    from rclpy.executors import SingleThreadedExecutor
    from rclpy.node import Node
    from rclpy.signals import SignalHandlerOptions
    from rclpy.utilities import remove_ros_args
    import sys
    parser = argparse.ArgumentParser(description='Native Android WSS ROS receiver: USB or wireless')
    parser.add_argument('--cert', required=True)
    parser.add_argument('--key', required=True)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8443)
    parser.add_argument('--calibration', default='')
    config = parser.parse_args(remove_ros_args(args=sys.argv)[1:])
    tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    tls.minimum_version = ssl.TLSVersion.TLSv1_2
    tls.load_cert_chain(config.cert, config.key)
    import hashlib
    pem = Path(config.cert).read_text()
    certificate = pem[:pem.index('-----END CERTIFICATE-----') + len('-----END CERTIFICATE-----')]
    pin = hashlib.sha256(ssl.PEM_cert_to_DER_cert(certificate)).hexdigest()
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    node = Node('phone_bridge')
    if node.get_parameter('use_sim_time').value:
        raise ValueError('Live phone bridge requires use_sim_time false')
    sink = RosSink(node, config.calibration)
    token = secrets.token_urlsafe(24)
    print('\nPAIRING TOKEN (this session only): ' + token, flush=True)
    print('ANDROID SERVER CERTIFICATE SHA-256: ' + pin, flush=True)
    print(f'Android: wss://YOUR_LAPTOP_ADDRESS:{config.port}/ws/android', flush=True)
    print(f'USB (after adb reverse): wss://127.0.0.1:{config.port}/ws/android', flush=True)
    print('Wireless: use the laptop address on the phone hotspot. Keep ROS local.', flush=True)
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()
    try:
        web.run_app(create_app(sink, token),
                    host=config.host, port=config.port, ssl_context=tls, access_log=None)
    finally:
        executor.shutdown()
        thread.join(timeout=5)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
