# Explain your reasoning

Written responses are self-assessed or reviewed by the instructor.

## Your robotics workbench

1. Explain Linux home, the filesystem root and the Windows C: mount. Show how to open Linux home in Windows Explorer.

Evidence: Include pwd output and identify a suitable path for ros2_ws.

Model explanation: / is the root of the Linux directory tree; ~ expands to the current user’s home. /mnt/c exposes Windows C: under WSL. In Ubuntu, cd ~ then explorer.exe . opens Linux home in Explorer.

2. Explain what the turtle test proves and what the four-package build in lecture 02 will check separately.

Evidence: Include the observed node names and explain which terminal receives the arrow keys.

Model explanation: The test checks installed ROS tools, GUI support and keyboard-to-simulator communication. The later build checks supplied source layout, dependencies and package installation. New terminals load the Jazzy underlay through .bashrc; the course overlay exists only after a successful build.

## From a robot to the ROS graph

1. Explain the sensing–processing–actuation loop for a robot of your choice, and place ROS and the OS in your design.

Evidence: Draw labelled arrows and name one component ROS does not provide automatically.

Model explanation: Identify a measurement, a decision, a motor command and the changed world being measured again. The OS manages hardware/processes; ROS libraries and tools support the user-space nodes exchanging those data.

2. Draw the phone-to-laptop data path and label the boundary where a WebSocket packet becomes a ROS message.

Evidence: Name the image topic and type.

Model explanation: The Android app sends WSS packets to phone_bridge, which validates/decodes them and publishes typed ROS topics. The estimator subscribes through ROS.

3. A topic is listed but its subscriber is silent. Describe your diagnosis in an order that can distinguish a naming problem from a QoS problem.

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
