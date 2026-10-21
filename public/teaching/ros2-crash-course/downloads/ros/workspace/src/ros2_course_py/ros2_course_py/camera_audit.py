"""Inspect the four stereo inputs without copying or processing their pixels.

This basic audit checks recent messages, not exact synchronization or calibration.
Run with use_sim_time:=true for a bag publishing /clock.
"""
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image


def stamp_ns(message):
    return message.header.stamp.sec * 1_000_000_000 + message.header.stamp.nanosec


class CameraAudit(Node):
    def __init__(self):
        super().__init__('camera_audit')
        self.latest = {}
        self.arrival = {}
        self.subscriptions_ = []
        defaults = {
            'left_image': '/stereo/left/image_rect',
            'right_image': '/stereo/right/image_rect',
            'left_info': '/stereo/left/camera_info',
            'right_info': '/stereo/right/camera_info',
        }
        for key, topic in defaults.items():
            self.declare_parameter(key + '_topic', topic)
            msg_type = Image if key.endswith('image') else CameraInfo
            self.subscriptions_.append(self.create_subscription(
                msg_type, self.get_parameter(key + '_topic').value,
                lambda msg, name=key: self.receive(name, msg), qos_profile_sensor_data))
        self.timer_ = self.create_timer(1.0, self.report)

    def receive(self, name, message):
        self.latest[name] = message
        self.arrival[name] = time.monotonic()

    def report(self):
        missing = set(('left_image', 'right_image', 'left_info', 'right_info')) - self.latest.keys()
        if missing:
            self.get_logger().warn('Waiting for: ' + ', '.join(sorted(missing)))
            return
        left, right = self.latest['left_image'], self.latest['right_image']
        li, ri = self.latest['left_info'], self.latest['right_info']
        problems = []
        for name, msg in self.latest.items():
            if time.monotonic() - self.arrival[name] > 2.0:
                problems.append(name + ' not received for >2 wall seconds')
            if not msg.header.frame_id:
                problems.append(name + ' has empty frame_id')
            if stamp_ns(msg) == 0:
                problems.append(name + ' has a zero stamp')
        for side, image, info in [('left', left, li), ('right', right, ri)]:
            if (image.width, image.height) != (info.width, info.height):
                problems.append(side + ' resolution mismatch')
            if image.header.frame_id != info.header.frame_id:
                problems.append(side + ' image/CameraInfo frame mismatch')
            if image.width == 0 or image.height == 0 or len(image.data) != image.step * image.height:
                problems.append(side + ' empty or inconsistent image buffer')
            if not all(math.isfinite(v) for v in list(info.k) + list(info.p)) or info.k[0] <= 0:
                problems.append(side + ' invalid intrinsics/projection')
        fx = ri.p[0]
        baseline = -ri.p[3] / fx if math.isfinite(fx) and fx > 0 else float('nan')
        if not math.isfinite(baseline) or baseline <= 0:
            problems.append('invalid conventional right projection baseline')
        skew_ms = (max(stamp_ns(m) for m in self.latest.values()) -
                   min(stamp_ns(m) for m in self.latest.values())) / 1_000_000
        text = (
            f'{left.width}x{left.height} encoding={left.encoding}/{right.encoding} '
            f'frames={left.header.frame_id}/{right.header.frame_id} '
            f'fx={fx:.2f}px baseline={baseline:.4f}m recent stamp spread={skew_ms:.2f}ms; '
            'latest samples are not a synchronized tuple')
        if problems:
            self.get_logger().warn(text + '; ' + '; '.join(problems))
        else:
            self.get_logger().info(text)


def main(args=None):
    rclpy.init(args=args)
    node = CameraAudit()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            if rclpy.ok():
                rclpy.shutdown()
