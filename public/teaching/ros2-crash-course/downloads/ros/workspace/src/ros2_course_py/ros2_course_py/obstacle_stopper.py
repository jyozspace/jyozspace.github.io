#!/usr/bin/env python3
"""
Lecture 5 - the classic "sense -> think -> act" node.

Subscribes to /scan (sensor_msgs/LaserScan)
Publishes  to /cmd_vel (geometry_msgs/Twist)

Behaviour: drive forward; if something is closer than `stop_distance` inside the
front cone, stop and rotate until the path is clear.

Run in the Gazebo TurtleBot3 world:
    ros2 run ros2_course_py obstacle_stopper --ros-args -p use_sim_time:=true

SAFETY: this is a teaching example, not a safety system. On real hardware always
keep a hand on the e-stop / power switch.
"""

import math
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ObstacleStopper(Node):
    def __init__(self):
        super().__init__('obstacle_stopper')

        self.declare_parameter('stop_distance', 0.45)     # metres
        self.declare_parameter('forward_speed', 0.15)     # m/s
        self.declare_parameter('turn_speed', 0.5)         # rad/s
        self.declare_parameter('front_cone_deg', 30.0)    # +/- degrees about 0 rad

        self.cmd_pub_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_sub_ = self.create_subscription(
            LaserScan, 'scan', self.callback_scan, qos_profile_sensor_data
        )

        self.front_distance_ = float('inf')
        self.last_valid_scan_ = None
        self.control_timer_ = self.create_timer(0.1, self.control_loop)  # 10 Hz
        self.get_logger().info('Obstacle stopper running. Ctrl-C to stop.')

    def callback_scan(self, scan: LaserScan):
        """Reduce the whole scan to ONE number: min distance in the front cone."""
        half_cone = math.radians(self.get_parameter('front_cone_deg').value)

        best = float('inf')
        for i, r in enumerate(scan.ranges):
            if math.isinf(r) or math.isnan(r):
                continue
            if not (scan.range_min <= r <= scan.range_max):
                continue

            angle = scan.angle_min + i * scan.angle_increment
            # Wrap into [-pi, pi] so the cone test works for 0..2pi scanners too.
            angle = math.atan2(math.sin(angle), math.cos(angle))
            if abs(angle) <= half_cone:
                best = min(best, r)

        self.front_distance_ = best
        self.last_valid_scan_ = time.monotonic() if math.isfinite(best) else None

    def control_loop(self):
        cmd = Twist()
        # Optional simulation example: never drive on absent, stale or invalid data.
        if self.last_valid_scan_ is None or time.monotonic() - self.last_valid_scan_ > 0.5:
            self.cmd_pub_.publish(cmd)
            return
        stop_distance = self.get_parameter('stop_distance').value

        if self.front_distance_ < stop_distance:
            cmd.linear.x = 0.0
            cmd.angular.z = self.get_parameter('turn_speed').value
            self.get_logger().info(
                f'BLOCKED at {self.front_distance_:.2f} m - turning', throttle_duration_sec=1.0
            )
        else:
            cmd.linear.x = self.get_parameter('forward_speed').value
            cmd.angular.z = 0.0

        self.cmd_pub_.publish(cmd)

    def stop_robot(self):
        self.cmd_pub_.publish(Twist())   # all-zero Twist == stop


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleStopper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
