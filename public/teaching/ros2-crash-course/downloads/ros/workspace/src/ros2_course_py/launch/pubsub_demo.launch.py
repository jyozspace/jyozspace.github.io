"""
Lecture 4 - a launch file starts several nodes with one command.

Run:  ros2 launch ros2_course_py pubsub_demo.launch.py
      ros2 launch ros2_course_py pubsub_demo.launch.py message:="Namaste" rate:=5.0
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Launch ARGUMENTS let you change behaviour from the command line.
    message_arg = DeclareLaunchArgument('message', default_value='Hello from launch')
    rate_arg = DeclareLaunchArgument('rate', default_value='2.0')

    talker = Node(
        package='ros2_course_py',
        executable='params_demo',
        name='my_talker',                     # remap the node name
        parameters=[{
            'message': LaunchConfiguration('message'),
            'rate_hz': ParameterValue(LaunchConfiguration('rate'), value_type=float),
        }],
        remappings=[('chatter', 'lecture_chatter')],   # topic renamed for BOTH nodes
        output='screen',
    )

    listener = Node(
        package='ros2_course_py',
        executable='listener',
        name='my_listener',
        remappings=[('chatter', 'lecture_chatter')],
        output='screen',
    )

    return LaunchDescription([message_arg, rate_arg, talker, listener])
