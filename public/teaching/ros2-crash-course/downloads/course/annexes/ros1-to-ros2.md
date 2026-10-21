# Recognize an older tutorial

This course targets ROS 2 Jazzy. Older search results may use ROS 1 or a different ROS 2 distribution. Check the tutorial's version before installing or running anything.

## Translate the major concepts

| Older ROS 1 term or tool | ROS 2 course equivalent |
| --- | --- |
| roscore | No equivalent central master required for normal discovery |
| rospy / roscpp | rclpy / rclcpp |
| catkin workspace | colcon workspace with ament packages |
| rostopic | ros2 topic |
| rosnode | ros2 node |
| rosservice | ros2 service |
| rosparam | ros2 param, with parameters owned by nodes |
| rosrun | ros2 run |
| roslaunch XML | ros2 launch; Python, XML and YAML launch descriptions are available |
| rosbag | ros2 bag; formats and conversion need explicit attention |

## Keep the differences visible

ROS 2 endpoint QoS affects compatibility, unlike simply assuming TCPROS behavior. Nodes own their parameters. Executors and callback groups control callback scheduling. Many packages retained familiar names but changed APIs and launch arguments. A ROS 1 bag or package cannot be made ROS 2-compatible just by renaming it.

## Choose the right reference

Use the [official Jazzy tutorials](https://docs.ros.org/en/jazzy/Tutorials.html). Use Jazzy/Ubuntu 24.04 installation instructions so the platform and binary packages match.
