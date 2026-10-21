# Jazzy command field guide

Run these commands in Ubuntu 24.04 Bash. UPPERCASE names are placeholders. Source ROS in every terminal; source the overlay after it has been built.

## Environment and builds

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
unset ROS_LOCALHOST_ONLY
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export ROS_DOMAIN_ID=42
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
colcon build --packages-up-to ros2_course_py
colcon test
colcon test-result --verbose
```

Use --packages-up-to when dependencies may need rebuilding too. Keep environment settings consistent across terminals. Localhost-only ROS does not prevent the separate HTTPS server from listening on the laptop’s hotspot interface.

## Inspect the graph and its interfaces

```bash
ros2 node list
ros2 node info /phone_bridge
ros2 topic list -t
ros2 topic info /phone/camera/image_raw --verbose
ros2 topic hz /phone/camera/image_raw
ros2 topic echo /phone/camera/camera_info --once
ros2 topic echo /phone/imu/accelerometer --once --qos-reliability best_effort
ros2 topic echo /phone/imu/gyroscope --once --qos-reliability best_effort
ros2 interface show sensor_msgs/msg/Image
ros2 interface show sensor_msgs/msg/Imu
ros2 run image_view image_view --ros-args -r image:=/phone/camera/image_raw
```

Use verbose endpoint information for QoS. Topic hz measures what the tool receives. Avoid dumping full pixel arrays; inspect headers or CameraInfo when debugging time and calibration.

## Requests, goals and configuration

Start the appropriate server in another terminal first:

```bash
ros2 run ros2_course_py area_server
```

```bash
ros2 service call /compute_area ros2_course_interfaces/srv/ComputeRectangleArea \
  "{width: 3.0, height: 4.0}"
ros2 action list -t
ros2 action send_goal /count_until ros2_course_interfaces/action/CountUntil \
  "{target: 8, period: 0.5}" --feedback
ros2 param get /params_demo rate_hz
ros2 param set /params_demo rate_hz 5.0
ros2 launch ros2_course_py pubsub_demo.launch.py rate:=5.0
```

The service, action and parameter examples are separate demonstrations with their own running nodes. The action client’s --ros-args -p cancel_after:=2.0 option requests cancellation; closing a client is not a general cancellation guarantee.

## Phone capture and replay

```bash
ros2 run ros2_course_py phone_bridge \
  --cert ~/phone-lab/laptop.pem --key ~/phone-lab/laptop-key.pem \
  --calibration ~/phone-lab/camera.yaml
ros2 bag record -o ~/phone-lab/walk01 \
  /phone/camera/image_raw /phone/camera/camera_info \
  /phone/imu/accelerometer /phone/imu/gyroscope /phone/diagnostics
ros2 bag info ~/phone-lab/walk01
ros2 bag play ~/phone-lab/walk01 --clock --rate 0.5
```

These are commands for different terminals/stages. Stop the live bridge before replay. Relevant timestamp consumers use use_sim_time true for playback; the live bridge uses wall time. Use a fresh mapper process when replaying a new experiment.

## Frames and recovery

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo demo_base demo_sensor
ros2 doctor --report
echo $ROS_DISTRO
ros2 daemon stop
ros2 daemon start
```

The demo TF exists only after the lecture’s static publisher has started. The phone bridge leaves camera–IMU TF unspecified until that relationship is measured. Restarting the daemon may repair stale CLI discovery; it cannot repair a missing calibration or a genuinely incompatible QoS pair.
