#!/usr/bin/env python3
"""
Lecture 1/2 warm-up - make the turtlesim turtle drive a square.

Terminal 1:  ros2 run turtlesim turtlesim_node
Terminal 2:  ros2 run ros2_course_py turtle_square

This node is a pure publisher to /turtle1/cmd_vel. It shows a state machine
driven by a timer -- the standard way to write timed behaviour in ROS 2.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleSquare(Node):
    def __init__(self):
        super().__init__('turtle_square')

        self.declare_parameter('side_seconds', 2.0)
        self.declare_parameter('turn_seconds', 1.6)

        self.pub_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.state_ = 'DRIVE'
        self.elapsed_ = 0.0
        self.dt_ = 0.1
        self.timer_ = self.create_timer(self.dt_, self.tick)

    def tick(self):
        cmd = Twist()
        side = self.get_parameter('side_seconds').value
        turn = self.get_parameter('turn_seconds').value

        if self.state_ == 'DRIVE':
            cmd.linear.x = 1.5
            if self.elapsed_ >= side:
                self.state_, self.elapsed_ = 'TURN', 0.0
        else:
            cmd.angular.z = 1.0
            if self.elapsed_ >= turn:
                self.state_, self.elapsed_ = 'DRIVE', 0.0

        self.pub_.publish(cmd)
        self.elapsed_ += self.dt_


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSquare()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub_.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
