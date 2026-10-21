#!/usr/bin/env python3
"""
Lecture 4 - parameters: how you configure a node WITHOUT editing its source.

Run with defaults:
    ros2 run ros2_course_py params_demo

Override at launch time:
    ros2 run ros2_course_py params_demo --ros-args -p message:="Namaste" -p rate_hz:=5.0

Inspect and change at RUNTIME:
    ros2 param list
    ros2 param get /params_demo message
    ros2 param set /params_demo message "changed live!"
"""

import math

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import String


class ParamsDemo(Node):
    def __init__(self):
        super().__init__('params_demo')

        # declare_parameter(name, default_value) -- ALWAYS declare before you use.
        self.declare_parameter('message', 'Hello from a parameter')
        self.declare_parameter('rate_hz', 2.0)

        self.message_ = self.get_parameter('message').value
        rate_hz = self.get_parameter('rate_hz').value
        if not isinstance(rate_hz, float) or not math.isfinite(rate_hz) or not 0.1 <= rate_hz <= 100:
            raise ValueError('rate_hz must be a finite float in [0.1, 100]')

        self.pub_ = self.create_publisher(String, 'chatter', 10)
        self.timer_ = self.create_timer(1.0 / rate_hz, self.publish)
        self.rate_hz_ = rate_hz

        # This callback fires whenever someone runs `ros2 param set`.
        self.add_on_set_parameters_callback(self.on_param_change)

        self.get_logger().info(f'Started with message="{self.message_}", rate={rate_hz} Hz')

    def on_param_change(self, params):
        # Validate the whole transaction before applying any side effect.
        for p in params:
            if p.name == 'rate_hz' and (
                    not isinstance(p.value, float) or not math.isfinite(p.value)
                    or not 0.1 <= p.value <= 100.0):
                return SetParametersResult(
                    successful=False, reason='rate_hz must be a float in [0.1, 100]')
            if p.name == 'message' and not isinstance(p.value, str):
                return SetParametersResult(successful=False, reason='message must be a string')
        return SetParametersResult(successful=True)

    def apply_param_change(self, params):
        for p in params:
            if p.name == 'message' and p.value != self.message_:
                self.message_ = p.value
                self.get_logger().info(f'message updated to "{self.message_}"')
            elif p.name == 'rate_hz' and p.value != self.rate_hz_:
                self.destroy_timer(self.timer_)
                self.rate_hz_ = p.value
                self.timer_ = self.create_timer(1.0 / p.value, self.publish)

    def publish(self):
        # Read committed parameters here, after
        # validation/acceptance, and apply changes at the next existing timer tick.
        self.apply_param_change([self.get_parameter('message'), self.get_parameter('rate_hz')])
        msg = String()
        msg.data = self.message_
        self.pub_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ParamsDemo()
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
