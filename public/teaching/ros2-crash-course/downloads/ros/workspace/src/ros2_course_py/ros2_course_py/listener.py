#!/usr/bin/env python3
"""
Lecture 2 - the matching subscriber.

Run it with:  ros2 run ros2_course_py listener
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ListenerNode(Node):
    """A node that subscribes to /chatter and prints whatever arrives."""

    def __init__(self):
        super().__init__('py_listener')

        # create_subscription(msg_type, topic_name, callback, qos_depth)
        # The callback runs on the executor thread every time a message arrives.
        self.subscription_ = self.create_subscription(
            String,
            'chatter',
            self.callback_chatter,
            10,
        )

        self.get_logger().info('Listener has been started, waiting for messages...')

    def callback_chatter(self, msg: String):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = ListenerNode()
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
