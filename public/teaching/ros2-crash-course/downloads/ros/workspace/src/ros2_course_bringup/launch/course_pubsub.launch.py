"""Include the beginner Python launch recipe from a system bringup package."""
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    launch_file = Path(get_package_share_directory('ros2_course_py')) / 'launch' / 'pubsub_demo.launch.py'
    return LaunchDescription([IncludeLaunchDescription(PythonLaunchDescriptionSource(str(launch_file)))])
