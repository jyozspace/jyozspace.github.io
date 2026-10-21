# Primary references and next steps

The course target is Jazzy / Ubuntu 24.04. Use distribution-specific documentation and record third-party versions for the phone backend.

## ROS foundations

- [Jazzy tutorials](https://docs.ros.org/en/jazzy/Tutorials.html): CLI, client libraries, launch, interfaces and TF2.
- [Jazzy Ubuntu installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html): supported binaries and repository setup.
- [Jazzy rclpy source](https://github.com/ros2/rclpy/tree/jazzy): inspect the implementation behind client-library behavior.
- [QoS policies](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html): directional compatibility and durability.
- [REP 103](https://www.ros.org/reps/rep-0103.html) and [REP 105](https://www.ros.org/reps/rep-0105.html): units, axes and mobile frame semantics.

## A small vocabulary to keep nearby

| Term | Meaning in this course |
| --- | --- |
| Callback / executor | A function invoked for ready work / the component that schedules and runs it |
| Header | Message metadata carrying a timestamp and coordinate-frame name |
| QoS | Delivery and storage policies that must be compatible between endpoints |
| Intrinsics / extrinsics | A camera’s pixel-to-ray model / the geometric relationship between sensors or frames |
| Latency / rate | Delay between events / number of samples per second; a high rate can still have large delay |
| Radian | Angular unit: a full turn is 2π radians, so 180 degrees is π radians |
| Sparse / dense reconstruction | Selected scene landmarks / much more complete surface sampling or geometry |
| Scale ambiguity | Monocular reconstruction can preserve relative shape without knowing its size in metres |
| Sensor fusion | Combining measurements in an estimator using their models, timing and uncertainty |
| Ground truth | An independent reference used to evaluate an estimate |

## Native Android acquisition and WSL

- [Camera2 overview](https://developer.android.com/media/camera/camera2): camera configuration and capture APIs.
- [Camera timestamp source](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics#SENSOR_INFO_TIMESTAMP_SOURCE): REALTIME and UNKNOWN clock meanings.
- [SensorEvent](https://developer.android.com/reference/android/hardware/SensorEvent): per-event time, device axes and motion units.
- [Android build and signing](https://developer.android.com/studio/publish/app-signing): package identity and APK distribution.
- [ADB reverse](https://developer.android.com/develop/ui/views/layout/webapps/access-local-server): USB port forwarding.
- [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking): localhost, mirrored networking and NAT forwarding.

## Calibration and visual mapping

- [image_pipeline Jazzy](https://github.com/ros-perception/image_pipeline/tree/jazzy): monocular calibration tools.
- [OpenCV calibration](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html): pinhole models and reprojection geometry.
- [ORB-SLAM3 upstream](https://github.com/UZ-SLAMLab/ORB_SLAM3): the existing sparse SLAM engine used by the optional adapter. Its build dependencies and license are separate from ROS course packages.
- [OpenVINS calibration](https://docs.openvins.com/gs-calibration.html): camera–IMU timing/extrinsics requirements for advanced inertial estimation.

## Guided annexes

- [Annex A: Build the Android app](../annexes/android-development.md): install/build the APK and inspect Camera2, SensorManager, timestamp metadata and cleanup.
- [Annex B: Build the ROS receiver](../annexes/bridge-development.md): trace protocol validation, OpenCV decoding, headers and publication.
- [Annex C: Camera & IMU calibration](../annexes/calibration.md): measure camera intrinsics, validate a model and plan a qualified inertial workflow.
- [Annex D: More ROS workflows](../annexes/ros-workflows.md): practice services, actions, recording/replay, TF, launch and parameters.
- [Annex E: Android USB or wireless](../annexes/android-connections.md): connect the same APK and receiver over a cable or a phone hotspot.
- [Annex F: Capstone on WSL 2](../annexes/wsl-capstone.md): choose a USB or Wi-Fi route and verify the Windows/Ubuntu boundaries.
- [Visual checkpoints](../annexes/visual-guide.md): compare your own output with labelled illustrative examples.

## After the crash course

Learn URDF/robot_state_publisher, lifecycle management, integration testing and deployment. Study [robot_localization](https://docs.ros.org/en/jazzy/p/robot_localization/) and [Nav2](https://docs.nav2.org/) after your metric sensor/TF contracts are established. Consult the [ROS/Gazebo compatibility table](https://gazebosim.org/docs/latest/ros_installation/) before adding simulation. Jazzy’s recommended modern pairing is Gazebo Harmonic. The simulator is an optional extension after the core course.
