# Course scope and verification

Reviewed 21 October 2026. This page tells learners and instructors what the examples demonstrate and which practical checks need a teaching machine. The course targets **ROS 2 Jazzy on Ubuntu 24.04**.

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

## How the material is checked

The build checks that downloadable pages match their source, quiz scenarios have context and explanatory feedback, answer indices are valid and every lesson has descriptive prompts. Source checks cover JavaScript syntax and Python example logic. Synthetic tests exercise the native version-2 protocol, receiver behavior, removal of legacy endpoints and calibration conversion. The Android APK has been compiled and signature-verified; its exact Java transport has been tested over local pinned TLS against the actual receiver, including wrong-pin/token rejection. See maintenance/docs/TESTING.md in the source folder for commands and execution scope.

The questions ask for a prediction or diagnosis in a stated situation. Written prompts request an explanation and evidence, with model responses for comparison. Those responses are self- or instructor-assessed. Passing a multiple-choice checkpoint is a reason to try the practical task, and collect evidence from the hardware task itself.

## How to interpret the illustrations

Software examples are labelled **simulated**. They illustrate topic names, fields and places to inspect; their rates, counts, timing and map points are examples. The equipment picture is an AI-generated conceptual illustration. A learner’s own terminal output, calibration record and real viewer screenshot provide evidence for their run. Open any figure to inspect it at full size.

## Official sources behind the guide

- [Jazzy release](https://discourse.ros.org/t/ros-2-jazzy-jalisco-released/37862), [installation source](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst) and [REP 2000](https://www.ros.org/reps/rep-2000.html): distribution support and platforms.
- [Jazzy rclpy](https://github.com/ros2/rclpy/tree/jazzy), [QoS documentation](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) and [cv_bridge changelog](https://github.com/ros-perception/vision_opencv/blob/rolling/cv_bridge/CHANGELOG.rst): client APIs, communication compatibility and header migration.
- [Jazzy camera calibration](https://github.com/ros-perception/image_pipeline/tree/jazzy/camera_calibration), [REP 103](https://www.ros.org/reps/rep-0103.html) and [REP 105](https://www.ros.org/reps/rep-0105.html): image calibration, units and frame meanings.
- [Android Camera2](https://developer.android.com/media/camera/camera2), [camera timestamp source](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics#SENSOR_INFO_TIMESTAMP_SOURCE), [SensorEvent](https://developer.android.com/reference/android/hardware/SensorEvent) and [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking): native acquisition, clock domains, device axes and connection routes.
- [ORB-SLAM3 public interface](https://github.com/UZ-SLAMLab/ORB_SLAM3/blob/master/include/System.h), [OpenVINS calibration](https://docs.openvins.com/gs-calibration.html) and [Kalibr](https://github.com/ethz-asl/kalibr/wiki): mapper input contracts and calibration requirements.

Some rendered ROS pages restrict automated access; their official repository sources are also linked. Record the revisions used for a classroom backend, since a moving source branch alone is insufficient to reproduce a build.

## Qualify the classroom run

This authoring environment supports static, synthetic and browser-layout checks. A real Ubuntu Jazzy/colcon build, external ORB-SLAM3 compilation, Android Camera2/SensorManager behavior, permissions, WSL/hotspot/USB reachability, phone TLS pairing, measured calibration and actual sparse mapping still need testing on the teaching equipment. The supplied optional adapter has not been compiled against an engine on this Windows host.

Phone lab setup contains the practical preflight. Before class, prepare a qualified phone run, matching camera calibration and a consented reference bag for students whose devices cannot supply the required streams. Actual recordings, engine binaries and vocabulary are acquired during that preparation; they are separate from the supplied source bundles.
