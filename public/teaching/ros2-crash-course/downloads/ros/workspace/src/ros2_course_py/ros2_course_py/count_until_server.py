#!/usr/bin/env python3
"""
Lecture 4 - an ACTION server: a long job with feedback and the ability to cancel.

Run:  ros2 run ros2_course_py count_until_server
Send: ros2 action send_goal /count_until ros2_course_interfaces/action/CountUntil \
        "{target: 8, period: 0.5}" --feedback
"""

import math
import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from ros2_course_interfaces.action import CountUntil


class CountUntilServer(Node):
    def __init__(self):
        super().__init__('count_until_server')

        self.action_server_ = ActionServer(
            self,
            CountUntil,
            'count_until',
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
        )
        self.get_logger().info('CountUntil action server started.')

    def goal_callback(self, goal_request):
        """Decide whether to accept the goal at all."""
        self.get_logger().info(f'Received goal: target={goal_request.target}')
        if (goal_request.target <= 0 or not math.isfinite(goal_request.period)
                or not 0.0 < goal_request.period <= 5.0):
            self.get_logger().warn('Rejecting: target > 0 and finite period in (0, 5] required.')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Cancel requested.')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Do the actual work. This runs in its own thread."""
        target = goal_handle.request.target
        period = goal_handle.request.period

        feedback = CountUntil.Feedback()
        result = CountUntil.Result()

        counter = 0
        for i in range(target):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.reached_number = counter
                self.get_logger().info('Goal canceled.')
                return result

            counter += 1
            feedback.current_number = counter
            goal_handle.publish_feedback(feedback)   # <- streamed to the client
            self.get_logger().info(f'count = {counter}')
            time.sleep(period)

        goal_handle.succeed()
        result.reached_number = counter
        return result


def main(args=None):
    rclpy.init(args=args)
    node = CountUntilServer()
    # An action server that sleeps needs more than one thread, or cancel requests
    # would never be processed.
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.action_server_.destroy()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
