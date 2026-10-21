#!/usr/bin/env python3
"""
Lecture 4 - the matching ACTION client.

Run:  ros2 run ros2_course_py count_until_client --ros-args -p target:=6
"""

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from ros2_course_interfaces.action import CountUntil


class CountUntilClient(Node):
    def __init__(self):
        super().__init__('count_until_client')
        self.declare_parameter('target', 5)
        self.declare_parameter('period', 0.7)
        self.declare_parameter('cancel_after', 0.0)
        self.cancel_timer_ = None
        self.goal_handle_ = None

        self.action_client_ = ActionClient(self, CountUntil, 'count_until')

    def send_goal(self):
        self.action_client_.wait_for_server()

        goal = CountUntil.Goal()
        goal.target = self.get_parameter('target').value
        goal.period = self.get_parameter('period').value

        self.get_logger().info(f'Sending goal: count to {goal.target}')
        self.action_client_ \
            .send_goal_async(goal, feedback_callback=self.feedback_callback) \
            .add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal was REJECTED by the server.')
            if rclpy.ok():
                rclpy.shutdown()
            return
        self.get_logger().info('Goal accepted.')
        self.goal_handle_ = goal_handle
        cancel_after = self.get_parameter('cancel_after').value
        if cancel_after > 0.0:
            self.cancel_timer_ = self.create_timer(cancel_after, self.cancel_goal)
        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def cancel_goal(self):
        self.cancel_timer_.cancel()
        self.goal_handle_.cancel_goal_async()
        self.get_logger().info('Cancellation requested; waiting for terminal result.')

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'feedback: {feedback_msg.feedback.current_number}')

    def result_callback(self, future):
        result = future.result().result
        status = future.result().status
        status_name = {4: 'succeeded', 5: 'canceled', 6: 'aborted'}.get(status, str(status))
        self.get_logger().info(f'Terminal action status: {status_name}')
        self.get_logger().info(f'FINAL RESULT: reached {result.reached_number}')
        if rclpy.ok():
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClient()
    node.send_goal()
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
