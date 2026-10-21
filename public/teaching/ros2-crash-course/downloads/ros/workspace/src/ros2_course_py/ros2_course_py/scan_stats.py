#!/usr/bin/env python3
"""
Lecture 5 - reading a real sensor topic: sensor_msgs/msg/LaserScan.

Prints the closest obstacle and the distance straight ahead, once per second.

Run:  ros2 run ros2_course_py scan_stats
      ros2 run ros2_course_py scan_stats --ros-args -p use_sim_time:=true   # in Gazebo

KEY IDEA -- a LaserScan is ONE array of distances, plus the geometry needed to
know which direction each number points in:

    angle of ranges[i] = angle_min + i * angle_increment      (radians, CCW)

    ranges[0]                 -> angle_min   (often straight behind or right)
    ranges[len//2]            -> the middle of the sweep
    index for angle theta     -> int((theta - angle_min) / angle_increment)

Values may be inf or nan -- ALWAYS filter them out before doing maths.
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


class ScanStats(Node):
    def __init__(self):
        super().__init__('scan_stats')

        # qos_profile_sensor_data == BEST_EFFORT reliability + small queue.
        # Most real drivers publish sensor data BEST_EFFORT. If you subscribe with
        # the default RELIABLE profile you will silently receive NOTHING.
        self.sub_ = self.create_subscription(
            LaserScan, 'scan', self.callback_scan, qos_profile_sensor_data
        )

        self.last_scan_ = None
        self.timer_ = self.create_timer(1.0, self.report)
        self.get_logger().info('Waiting for /scan ...')

    def callback_scan(self, msg: LaserScan):
        self.last_scan_ = msg

    @staticmethod
    def range_at_angle(scan: LaserScan, angle_rad: float):
        """Return the measured distance at `angle_rad`, or None if unusable."""
        if not scan.ranges or scan.angle_increment <= 0.0:
            return None
        if angle_rad < scan.angle_min or angle_rad > scan.angle_max:
            return None
        index = int(round((angle_rad - scan.angle_min) / scan.angle_increment))
        index = max(0, min(index, len(scan.ranges) - 1))
        value = scan.ranges[index]
        if math.isinf(value) or math.isnan(value):
            return None
        if value < scan.range_min or value > scan.range_max:
            return None
        return value

    def report(self):
        scan = self.last_scan_
        if scan is None:
            self.get_logger().warn('No scan received yet.')
            return

        valid = [
            r for r in scan.ranges
            if not math.isinf(r) and not math.isnan(r)
            and scan.range_min <= r <= scan.range_max
        ]

        if not valid:
            self.get_logger().warn('Scan received but every reading was invalid.')
            return

        front = self.range_at_angle(scan, 0.0)
        front_txt = f'{front:.2f} m' if front is not None else 'no return'

        self.get_logger().info(
            f'beams={len(scan.ranges)}  valid={len(valid)}  '
            f'closest={min(valid):.2f} m  farthest={max(valid):.2f} m  '
            f'front(0 rad)={front_txt}  '
            f'fov={math.degrees(scan.angle_max - scan.angle_min):.0f} deg'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ScanStats()
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
