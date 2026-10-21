# Explain your reasoning

Written responses are self-assessed or reviewed by the instructor.

## Your robotics workbench

1. Describe the underlay and overlay you source in a new terminal, including their order and why each is needed.

Evidence: Include your executable-list output.

Model explanation: Source /opt/ros/jazzy/setup.bash for ROS, then ~/ros2_ws/install/setup.bash for built course packages. Explain that environment changes are per terminal.

2. Explain which laptop components and pairing information are needed after installing the Android APK.

Evidence: Draw the two machines and identify where each program runs.

Model explanation: The laptop runs the updated ROS receiver with TLS and a session token. The APK needs its reachable /ws/android endpoint, certificate fingerprint and token. The optional mapper additionally needs its prepared engine and measured settings.

## Think in nodes and messages

1. Draw the phone-to-laptop data path and label the boundary where a WebSocket packet becomes a ROS message.

Evidence: Name the image topic and type.

Model explanation: The Android app sends WSS packets to phone_bridge, which validates/decodes them and publishes typed ROS topics. The estimator subscribes through ROS.

2. A topic is listed but its subscriber is silent. Describe your diagnosis in an order that can distinguish a naming problem from a QoS problem.

Evidence: Include one relevant CLI command for each stage.

Model explanation: Check live processes, resolved names/types, verbose endpoints and QoS, then data and environment/network configuration. Collect evidence at each stage so the diagnosis identifies the failing contract.

## Write your first Python nodes

1. Explain how init, Node construction, subscription/timer callbacks, spin and cleanup cooperate in your smallest node.

Evidence: Point to those operations in your code.

Model explanation: init establishes ROS context; the Node owns interfaces; the executor dispatches callbacks during spin; cleanup destroys the node and shuts down the context.

2. Your message counter grows irregularly at startup. Explain why this need not prove message loss and what extra evidence you would collect.

Evidence: Provide a short sample of counts and measured topic rate.

Model explanation: Discovery/startup delays and report boundaries affect the count. Compare sequence/rate evidence, QoS and process load before concluding that samples were lost.

## The same graph, in C++

1. Explain why a larger queue does not solve an incompatible reliable-request/best-effort-offer pair.

Evidence: Use offered and requested terminology in your answer.

Model explanation: Queue depth concerns retained samples; reliability compatibility concerns whether the publisher can meet the requested policy. Fix the policy contract, then consider buffering separately.

2. Compare the same Python and C++ publisher without claiming that the simple result proves one language is faster.

Evidence: Report observed rate and at least two limitations.

Model explanation: Explain the common graph contract and identify confounders such as logging, compilation/build state, scheduler load and measurement overhead.

## Connect a complete system

1. Compute the demo point transform in words, then state which transform a lookup_transform(target, source, time) request returns.

Evidence: Include units and frame names, not just three numbers.

Model explanation: Rotate (1,0,0) by +90° about z to (0,1,0), then add (0.1,0,0.2). The lookup maps source coordinates into target coordinates at the requested time.

2. Explain why the phone bridge does not publish an identity TF from phone_android_device to phone_camera_optical_frame.

Evidence: Describe one physical axis-check experiment and its limitation.

Model explanation: The Android device axes and transmitted-image optical axes need a measured geometric relationship. A guessed transform would falsely assert calibration; proper VIO needs a measured relation and timing model.

## A phone that helps build a map

1. Explain the Android camera-to-viewer path and distinguish REALTIME camera timestamps, UNKNOWN callback fallback and the estimated phone-to-laptop clock offset.

Evidence: Name the image and native accelerometer/gyroscope topics, identify the camera clock source and state which stream the mapper consumes.

Model explanation: Describe Camera2 image capture, JPEG/WSS, validation/clock conversion, ROS Image, measured settings and the monocular engine viewer. REALTIME shares the SensorEvent phone clock; UNKNOWN uses a labelled image callback estimate. The network clock offset remains an estimate.

2. Report a short phone experiment without overstating its result. Include one failure, its evidence, your repair and the remaining limits.

Evidence: Attach a bag manifest, real screenshot and tracking-state evidence.

Model explanation: Document phone/OS/APK checksum, camera ID/size/clock source, calibration, RTT/rates, commands and bag. Separate transport evidence from sparse monocular mapping; explain the remaining inertial-calibration work.
