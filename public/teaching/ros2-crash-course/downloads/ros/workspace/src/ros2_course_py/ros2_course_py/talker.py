#!/usr/bin/env python3
"""
Lecture 2 - the simplest possible publisher.

Run it with:      ros2 run ros2_course_py talker
Watch the topic:  ros2 topic echo /chatter
"""

import rclpy                                  # the ROS 2 Python client library
from rclpy.node import Node                   # base class for every Python node
from std_msgs.msg import String               # the message type we will publish


class TalkerNode(Node):
    """A node that publishes a String on /chatter twice per second."""

    def __init__(self):
        # "py_talker" is the DEFAULT node name. It can be changed at runtime with
        #   ros2 run ros2_course_py talker --ros-args -r __node:=some_other_name
        super().__init__('py_talker')

        # create_publisher(msg_type, topic_name, qos_depth)
        # qos_depth = 10 means "keep the last 10 messages if the subscriber is slow"
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        self.counter_ = 0

        # A timer is how you do "run this every N seconds" in ROS 2.
        # A timer lets the executor dispatch periodic work alongside other callbacks.
        # Sleeping inside a callback occupies its executor thread.
        self.timer_ = self.create_timer(0.5, self.publish_message)

        # get_logger() gives you the ROS logging system: it goes to the console AND
        # to /rosout, so other tools can see it.
        self.get_logger().info('Talker has been started.')

    def publish_message(self):
        msg = String()
        msg.data = f'Hello ROS 2! count = {self.counter_}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.counter_ += 1


def main(args=None):
    rclpy.init(args=args)          # 1. start up the ROS 2 client library
    node = TalkerNode()            # 2. create the node
    try:
        rclpy.spin(node)           # 3. block here, letting timers/callbacks fire
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()        # 4. clean up
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
