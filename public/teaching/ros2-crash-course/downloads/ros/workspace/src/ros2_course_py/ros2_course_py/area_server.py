#!/usr/bin/env python3
"""
Lecture 4 - a SERVICE server (short request/response).

Run:  ros2 run ros2_course_py area_server
Call: ros2 service call /compute_area ros2_course_interfaces/srv/ComputeRectangleArea "{width: 3.0, height: 4.0}"
"""

import math

import rclpy
from rclpy.node import Node
from ros2_course_interfaces.srv import ComputeRectangleArea


class AreaServer(Node):
    def __init__(self):
        super().__init__('area_server')

        # create_service(srv_type, service_name, callback)
        self.srv_ = self.create_service(
            ComputeRectangleArea,
            'compute_area',
            self.callback_compute_area,
        )
        self.get_logger().info('Area service is ready.')

    def callback_compute_area(self, request, response):
        # A service callback MUST fill in `response` and return it.
        # Keep it FAST -- while it runs, the node is busy.
        if (not math.isfinite(request.width) or not math.isfinite(request.height)
                or request.width < 0.0 or request.height < 0.0
                or not math.isfinite(request.width * request.height)):
            response.area = 0.0
            response.valid = False
            response.message = 'dimensions and area must be finite; dimensions must be >= 0'
        else:
            response.area = request.width * request.height
            response.valid = True
            response.message = 'ok'

        self.get_logger().info(
            f'{request.width} x {request.height} -> {response.area}'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AreaServer()
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
