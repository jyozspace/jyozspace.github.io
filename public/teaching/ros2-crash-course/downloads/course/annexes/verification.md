# Course scope and learning outcomes

This course teaches **ROS 2 Jazzy on Ubuntu 24.04** through five lectures and a phone-sensor project.

## What you can learn here

The five lectures introduce graph inspection, Python/C++ nodes, interfaces, QoS, services, actions, parameters, launch, TF and sensor integration. Setup is separate from contact time. The full plan is four 90-minute lectures and one 180-minute project session; a five-by-90-minute delivery moves the mapping lab into follow-up practice.

The capstone connects a native Android sensor app to a ROS receiver. The same APK connects by wired USB or wireless. Its optional ORB-SLAM3 adapter creates a sparse monocular reconstruction with arbitrary scale. Native accelerometer/gyroscope events retain separate timestamps and are published for inspection. Annex C explains the acquisition and calibration requirements for a future visual-inertial project.

## Find the explanation you need

| Your question | Start here |
| --- | --- |
| What do I install and what is a sourced terminal? | Before you begin |
| What should my terminal or viewer show? | Visual checkpoints and the figures beside each exercise |
| How do I create, install and connect nodes? | Lectures 1–3 and the source browser |
| How do I request work and track progress? | Lecture 4 and Annex D’s service/action experiments |
| How do coordinate frames and timestamps work together? | Frames, transforms & time |
| How is the app developed? | Annex A: Build the Android app |
| How does web data become a ROS message? | Annex B: Build the ROS receiver |
| How do I measure camera calibration and inspect inertial data? | Annex C: Camera & IMU calibration |
| How do I repeat an experiment or go further? | Annex D and Keep learning |

## Practice and assessment

Each lesson includes predictions, practical exercises and written explanations. Attempt the exercises before consulting the worked responses. Use your own terminal output, frame graph, camera measurements and recordings to explain your results. Quiz progress and notes are stored in your browser and can be exported from Resources.

## How to interpret the illustrations

Software examples are labelled **simulated**. They illustrate topic names, fields and places to inspect; their rates, counts, timing and map points are examples. The equipment picture is an AI-generated conceptual illustration. A learner’s own terminal output, calibration record and real viewer screenshot provide evidence for their run. Open any figure to inspect it at full size.

## Prepare for the capstone

Follow Phone lab setup before the project session. Prepare an Android phone, a working USB or wireless connection, camera calibration for the exact transmitted image mode and a consented reference recording. The optional mapping adapter additionally requires a separately built ORB-SLAM3 engine, vocabulary and matching camera settings.

The mapping result is a sparse monocular reconstruction with arbitrary scale. Receiving accelerometer and gyroscope messages does not establish metric scale or a calibrated visual-inertial estimator. Device compatibility, camera timing and measured calibration must be checked on the equipment you use.

## Official sources behind the guide

- [Jazzy release](https://discourse.ros.org/t/ros-2-jazzy-jalisco-released/37862), [installation source](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst) and [REP 2000](https://www.ros.org/reps/rep-2000.html): distribution support and platforms.
- [Jazzy rclpy](https://github.com/ros2/rclpy/tree/jazzy), [QoS documentation](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) and [cv_bridge changelog](https://github.com/ros-perception/vision_opencv/blob/rolling/cv_bridge/CHANGELOG.rst): client APIs, communication compatibility and header migration.
- [Jazzy camera calibration](https://github.com/ros-perception/image_pipeline/tree/jazzy/camera_calibration), [REP 103](https://www.ros.org/reps/rep-0103.html) and [REP 105](https://www.ros.org/reps/rep-0105.html): image calibration, units and frame meanings.
- [Android Camera2](https://developer.android.com/media/camera/camera2), [camera timestamp source](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics#SENSOR_INFO_TIMESTAMP_SOURCE), [SensorEvent](https://developer.android.com/reference/android/hardware/SensorEvent) and [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking): native acquisition, clock domains, device axes and connection routes.
- [ORB-SLAM3 public interface](https://github.com/UZ-SLAMLab/ORB_SLAM3/blob/master/include/System.h), [OpenVINS calibration](https://docs.openvins.com/gs-calibration.html) and [Kalibr](https://github.com/ethz-asl/kalibr/wiki): mapper input contracts and calibration requirements.
