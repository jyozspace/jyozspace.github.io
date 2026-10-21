import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'ros2_course_py'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # This line is what makes `ros2 launch ros2_course_py <file>` work.
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Instructor',
    maintainer_email='instructor@example.com',
    description='Python (rclpy) example nodes for the 5-session ROS 2 course.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        # LEFT of '=' is the name you type after `ros2 run ros2_course_py ...`
        # RIGHT of '=' is <python module path>:<function to call>
        'console_scripts': [
            'phone_bridge = ros2_course_py.phone_bridge:main',
            'camera_audit           = ros2_course_py.camera_audit:main',
            'talker                 = ros2_course_py.talker:main',
            'listener               = ros2_course_py.listener:main',
            'robot_status_publisher = ros2_course_py.robot_status_publisher:main',
            'params_demo            = ros2_course_py.params_demo:main',
            'area_server            = ros2_course_py.area_server:main',
            'area_client            = ros2_course_py.area_client:main',
            'count_until_server     = ros2_course_py.count_until_server:main',
            'count_until_client     = ros2_course_py.count_until_client:main',
            'scan_stats             = ros2_course_py.scan_stats:main',
            'obstacle_stopper       = ros2_course_py.obstacle_stopper:main',
            'tf_echo_demo           = ros2_course_py.tf_echo_demo:main',
            'turtle_square          = ros2_course_py.turtle_square:main',
        ],
    },
)
