# Worked explanations and assessment guide

Attempt the task before comparing. Evidence and reasoning matter more than recalling an isolated command. The generated descriptive-questions.md contains a model explanation and requested evidence for every written checkpoint.

## Lecture 1: graph and naming

Teleop publishes Twist on /turtle1/cmd_vel; turtlesim receives commands there and publishes Pose on /turtle1/pose. Under /robot2, relative names gain that namespace. Remapping only one endpoint disconnects a previously shared stream. The phone itself is a web client; phone_bridge is the node in the ROS graph.

Accept a diagram supported by node list, topic list -t and verbose endpoint output. A moving-turtle screenshot illustrates behavior; node/topic evidence explains the connection that produced it.

## Lecture 2: callbacks and interfaces

Use the complete publisher and subscriber in the lesson. In a subscription callback increment a node counter; use a timer to report the count. At approximately 2 Hz, a one-second report usually observes about two new messages, but startup/discovery and interval boundaries can vary.

For temperature_c homework, modify the .msg, regenerate interfaces, rebuild consumers and source the overlay. A .msg file is source for generated code, not an immediately available Python class.

## Lecture 3: QoS reasoning

A best-effort publisher cannot meet a reliable subscriber’s requested reliability. The reverse pair is compatible when other policies agree. Depth and durability are separate policies; a larger queue cannot fix incompatible reliability. Python/C++ interoperability depends on ROS contracts, not matching source syntax.

For the 5 Hz C++ exercise, a 200 ms timer is the nominal period. Rebuild the installed executable. Discuss logging and scheduler/measurement overhead before making performance claims.

## Lecture 4: services, parameters and transforms

The area request 3 by 4 returns 12 with valid true. The service does not provide an application-level exactly-once transaction guarantee. The action example has a goal, streamed feedback and a terminal result; use the supplied client’s cancel_after parameter to request cancellation and confirm canceled status.

The node validates updates without side effects, then reads committed values and adjusts its timer at the next existing timer tick. Explain the difference between accepting a parameter value and applying it to a running resource. Jazzy also offers post-set callbacks for designs that need an explicit application hook.

For the +90° sensor demo, rotate (1,0,0) to (0,1,0), then add (0.1,0,0.2): the result is (0.1,1.0,0.2) m in demo_base. lookup_transform(target, source, time) maps source coordinates into target. An identity quaternion is (0,0,0,1), and changing frame_id alone does not transform a point.

## Lecture 5: phone integration

The Android app checks the receiver certificate pin and session token over WSS. Option 1 uses wired USB with ADB reverse; Option 2 uses wireless over the phone hotspot. Both run the same app and version-2 WSS protocol, with the same pin, token and ROS topics. Hotspots separate local addressing while sharing radio airtime. A low RTT helps estimate phone-to-laptop offset; the camera’s timestamp source and sensor calibration need their own evidence.

Android accelerometer and gyroscope components retain separate event timestamps and m/s² or rad/s units under phone_android_device. Each ROS message marks its missing component unavailable. Camera–IMU geometry must be measured. The supplied backend consumes images and creates a sparse arbitrary-scale monocular reconstruction. The Pangolin map, current tracked-point cloud and bounded ROS pose history are different outputs.

## Capstone evidence and rubric

Submit the mode/version/calibration manifest, trusted connection and topic-rate evidence, a short consented bag with checksums, exact commands, mapping evidence from a qualified live/reference run, and one diagnosed failure. A useful deliberate fault is a wrong topic remap or invalid pairing token, repaired using concrete observations and explain which observation identified the fault.

Rubric: transport 25%; time/frame/calibration reasoning 30%; reproducibility/mapping evidence 25%; diagnosis and limits 20%. Learners with unsupported phones should analyze the instructor-prepared qualified reference run. Award credit for evidence that distinguishes sensor transport, sparse monocular reconstruction and the additional requirements of inertial estimation.
