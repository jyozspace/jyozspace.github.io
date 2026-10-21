#!/usr/bin/env python3
"""
Lecture 4 - a SERVICE client.

Run:  ros2 run ros2_course_py area_client --ros-args -p width:=5.0 -p height:=2.5

The important idea: `call_async()` returns a Future. You must let the executor
spin until the future is done -- otherwise you will wait forever.
"""

import rclpy
from rclpy.node import Node
from ros2_course_interfaces.srv import ComputeRectangleArea


class AreaClient(Node):
    def __init__(self):
        super().__init__('area_client')

        self.declare_parameter('width', 3.0)
        self.declare_parameter('height', 4.0)

        self.client_ = self.create_client(ComputeRectangleArea, 'compute_area')

        # Wait until a server actually exists, otherwise the call is dropped.
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Waiting for /compute_area service...')

    def send_request(self):
        request = ComputeRectangleArea.Request()
        request.width = self.get_parameter('width').value
        request.height = self.get_parameter('height').value

        future = self.client_.call_async(request)
        # spin_until_future_complete keeps the node alive until the answer arrives.
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        if response.valid:
            self.get_logger().info(f'Area = {response.area}')
        else:
            self.get_logger().error(f'Server said: {response.message}')


def main(args=None):
    rclpy.init(args=args)
    node = AreaClient()
    try:
        node.send_request()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
