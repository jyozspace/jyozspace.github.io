#!/usr/bin/env python3
"""
Lecture 2 / 4 - publishing a CUSTOM message type from ros2_course_interfaces.

Run:   ros2 run ros2_course_py robot_status_publisher
Check: ros2 topic echo /robot_status
       ros2 interface show ros2_course_interfaces/msg/RobotStatus
"""

import rclpy
from rclpy.node import Node
from ros2_course_interfaces.msg import RobotStatus


class RobotStatusPublisher(Node):
    def __init__(self):
        super().__init__('robot_status_publisher')

        self.pub_ = self.create_publisher(RobotStatus, 'robot_status', 10)
        self.battery_ = 100.0

        self.timer_ = self.create_timer(1.0, self.publish_status)
        self.get_logger().info('Robot status publisher started.')

    def publish_status(self):
        msg = RobotStatus()
        msg.robot_name = 'tb3_01'
        msg.battery_percent = self.battery_
        msg.is_moving = self.battery_ > 20.0
        msg.fault_code = 0 if self.battery_ > 10.0 else 7

        self.pub_.publish(msg)
        self.get_logger().info(
            f'battery={msg.battery_percent:.1f}%  moving={msg.is_moving}'
        )

        self.battery_ = max(0.0, self.battery_ - 2.5)


def main(args=None):
    rclpy.init(args=args)
    node = RobotStatusPublisher()
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
