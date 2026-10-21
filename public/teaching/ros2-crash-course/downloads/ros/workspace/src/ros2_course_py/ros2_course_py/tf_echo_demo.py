#!/usr/bin/env python3
"""
Lecture 4/5 - reading the TF tree from code.

Prints where the robot (base_link) is inside the map, once per second.

Run it while SLAM is running:
    ros2 run ros2_course_py tf_echo_demo --ros-args -p use_sim_time:=true

Equivalent one-liner from the terminal:
    ros2 run tf2_ros tf2_echo map base_link
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


def yaw_from_quaternion(q):
    """Convert a quaternion to a yaw angle (rotation about Z) in radians."""
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class TfEchoDemo(Node):
    def __init__(self):
        super().__init__('tf_echo_demo')

        self.declare_parameter('parent_frame', 'map')
        self.declare_parameter('child_frame', 'base_link')

        # The Buffer stores the last 10 s of transforms; the Listener fills it
        # from /tf and /tf_static.
        self.tf_buffer_ = Buffer()
        self.tf_listener_ = TransformListener(self.tf_buffer_, self)

        self.timer_ = self.create_timer(1.0, self.lookup)

    def lookup(self):
        parent = self.get_parameter('parent_frame').value
        child = self.get_parameter('child_frame').value

        try:
            # rclpy.time.Time() (all zeros) means "the latest available transform".
            tf = self.tf_buffer_.lookup_transform(
                parent, child, rclpy.time.Time(), timeout=Duration(seconds=0.0)
            )
        except TransformException as ex:
            self.get_logger().warn(f'Could not transform {parent} -> {child}: {ex}')
            return

        t = tf.transform.translation
        yaw = yaw_from_quaternion(tf.transform.rotation)
        self.get_logger().info(
            f'{child} in {parent}: x={t.x:+.2f} y={t.y:+.2f} yaw={math.degrees(yaw):+.1f} deg'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TfEchoDemo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
