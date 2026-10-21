# Course checkpoints

## Your robotics workbench

1. A learner has Ubuntu 22.04 and wants to follow this guide’s ROS 2 Jazzy binary installation commands. Which environment matches the course?

- A. Ubuntu 24.04 with ROS 2 Jazzy binaries
- B. Ubuntu 22.04 with a renamed Jazzy installation directory
- C. Ubuntu 24.04 with binaries from any ROS distribution

Answer: A. Jazzy’s Ubuntu binary target is Noble 24.04. Prepare that environment so the supported packages and course commands match.

2. The workspace built successfully yesterday. In a newly opened terminal ros2 cannot find ros2_course_py. What is the most direct next check?

- A. Regenerate every interface without inspecting the environment
- B. Source Jazzy and the workspace install/setup.bash in this terminal
- C. Delete the source package and reinstall the phone app

Answer: B. The overlay must be in this terminal’s environment. A successful build does not automatically source future terminals.

3. A student has installed the Android APK and configured adb reverse tcp:8443 tcp:8443 to a running laptop receiver. Which app address uses this wired USB route?

- A. wss://127.0.0.1:8443/ws/android, with the receiver fingerprint and token
- B. The public course website URL, because it hosts the APK download
- C. The phone hotspot gateway address, without a receiver port or token

Answer: A. ADB reverse forwards the phone localhost port over USB to the host receiver. The same APK uses the laptop hotspot address for wireless; both routes retain certificate pinning and the session token.

4. A class wants the phone-camera project to show a 3D reconstruction. Which pre-class preparation is required beyond installing the Android APK?

- A. A qualified backend, matching measured calibration, trusted network path and a rehearsed reference run
- B. Only installation of the APK, with no laptop receiver or calibration
- C. An arbitrary CameraInfo matrix copied from a different phone

Answer: A. The Android app transports measurements over USB or wireless. Calibration and a working SLAM engine are separate required dependencies.

## Think in nodes and messages

1. A native phone app sends JPEGs over WSS to a Python receiver that publishes Image messages. Which component participates directly in the ROS graph?

- A. The phone’s hotspot configuration page
- B. The ROS receiver node on the laptop
- C. Each individual JPEG file

Answer: B. The phone is a web sensor client; phone_bridge is the ROS participant publishing typed topics.

2. Two nodes appear in ros2 node list, but the turtle does not move. Which observation best establishes a correctly connected command stream?

- A. Both nodes use the same source language
- B. The publisher and subscriber resolve to the same topic/type with compatible QoS, and samples are observed
- C. Both programs were launched from the same directory

Answer: B. Process existence alone does not establish endpoint compatibility or data flow.

3. A second turtlesim is launched under namespace /robot2. Which command topic sends velocity commands to /robot2/turtle1?

- A. /robot2/turtle1/cmd_vel
- B. /turtle1/cmd_vel without any remapping
- C. /robot2 because all namespaced messages use one topic

Answer: A. The namespace prefixes the relative command-topic name. Namespaces do not merge all interfaces into one stream.

4. A publisher’s relative chatter name is remapped to camera_events, while its subscriber is unchanged. What behavior should you predict?

- A. The subscriber automatically follows the publisher’s new name
- B. Both endpoints connect because message types still match
- C. They are disconnected until their resolved topic names agree

Answer: C. Remapping is applied to individual endpoints. Type agreement cannot compensate for different resolved names.

5. You stop a velocity publisher with Ctrl+C while a physical base is moving. Which statement is appropriate before claiming the base is safely stopped?

- A. Process exit guarantees a zero command reaches the motor
- B. A zero command and independent stop/watchdog behavior must be considered
- C. Changing ROS_DOMAIN_ID immediately removes motor power

Answer: B. Software command delivery and actuator safety are different concerns. A stopped publisher need not stop a consumer.

## Write your first Python nodes

1. A timer callback contains a two-second sleep in a node spun by a single-threaded executor. What effect should you expect on that executor’s other ready callbacks?

- A. They can be delayed until the blocking callback returns
- B. They automatically move into separate operating-system processes
- C. Their topic names change to include the timer period

Answer: A. An executor cannot dispatch another callback on that same thread while the current one blocks.

2. You add temperature_c to RobotStatus.msg, but Python cannot import the changed generated type. Which workflow is needed?

- A. Edit only the publisher’s import statement
- B. Regenerate/build the interface and dependent consumers, then source the overlay
- C. Refresh the course page so it regenerates ROS messages

Answer: B. The .msg definition must be processed into generated code, and the resulting installation must be sourced.

3. The scratch hello.py runs with python3, but ros2 run my_camera_lab hello reports no executable. Which package configuration should you inspect?

- A. The console_scripts entry point, build/install result and sourced overlay
- B. The phone hotspot SSID only
- C. The name of the String message’s data field

Answer: A. Direct script execution and an installed ROS executable use different discovery paths.

4. A publisher requests a 0.5-second timer. Which measurement would be a reasonable expectation on an ordinary non-real-time student laptop?

- A. Exactly two samples in every subscriber interval, with no jitter
- B. An approximate 2 Hz stream, with scheduling and measurement variation
- C. A guaranteed 0.5-second network latency for every sample

Answer: B. A timer requests scheduling; it is not a hard timing or network-latency guarantee.

5. A student wants to describe a camera measurement with time and coordinate meaning. Which interface choice best supports downstream ROS tools?

- A. A String containing arbitrary unlabeled pixel text
- B. A standard Image with a meaningful Header plus matching CameraInfo
- C. A custom message whose only field is the node’s filename

Answer: B. Standard sensor interfaces make dimensions, encoding, time, frame and calibration contracts explicit.

## The same graph, in C++

1. A camera publisher offers best-effort reliability while a subscription requests reliable delivery. Other names and types match. What should you predict?

- A. A discovered topic may still deliver no samples to that incompatible subscription
- B. The subscriber forces the camera publisher to become reliable
- C. C++ subscribers bypass reliability compatibility

Answer: A. The offered reliability cannot meet the stronger request. Inspect verbose endpoint policies.

2. A publisher offers reliable delivery and the subscriber requests best effort. With all other policies compatible, what is expected?

- A. The pair is incompatible because the labels differ
- B. The reliability pair is compatible
- C. Only Python can connect these policies

Answer: B. A reliable offer meets the weaker best-effort request. The compatibility relation is directional.

3. A Python listener receives a C++ talker’s String messages. What actually makes this cross-language connection possible?

- A. The two source files have the same filename
- B. They share a resolved topic, compatible type/QoS and transport configuration
- C. The C++ program imports the Python class

Answer: B. ROS interfaces and middleware define the connection independently of source-language syntax.

4. You change the C++ timer period from 500 ms to 200 ms but still observe the old rate. Which first action addresses the likely cause?

- A. Rebuild the changed package and run the updated installed executable
- B. Change the image frame_id
- C. Increase the subscriber’s queue depth until it changes the publisher timer

Answer: A. C++ edits do not alter an existing installed binary. Build and verify the running executable.

5. A late-joining subscriber needs retained static transform information. Which policy should you inspect in addition to reliability?

- A. Editor indentation width
- B. Durability and retained-history compatibility
- C. The source language of the static publisher

Answer: B. Transient-local durability supports retained data for suitable late-joining subscriptions. Reliability alone does not describe retained history.

## Connect a complete system

1. A robot is asked to navigate for several minutes while reporting progress and accepting cancellation. Which ROS interaction best represents that job?

- A. An action with goal, feedback, cancellation handling and terminal result
- B. A short blocking service call with no progress protocol
- C. A parameter containing only the destination name

Answer: A. Actions explicitly represent long-running goal lifecycles. The server must still implement responsive cancellation.

2. The service request completes quickly and returns an area. What additional assumption would be incorrect when reasoning about failures and retries?

- A. The response has an application-defined validity field
- B. A service provides an application-level exactly-once transaction guarantee
- C. The callback should avoid blocking unrelated work

Answer: B. A service request/response is not a database transaction guarantee; application failure/retry semantics still matter.

3. A sensor is 0.1 m forward and 0.2 m above demo_base, yawed +90°. Its point (1,0,0) m is expressed in sensor coordinates. Where is it in demo_base?

- A. (1.1, 0, 0.2) m
- B. (0.1, 1.0, 0.2) m
- C. (0.1, -1.0, 0.2) m

Answer: B. Rotate the sensor’s positive x into base positive y, then add the mounting translation.

4. A ROS optical-frame point uses x right, y down and z forward. What must happen before interpreting it in a standard body frame?

- A. Rename its header.frame_id and keep all coordinates unchanged
- B. Apply the appropriate known transform, including its rotation
- C. Negate all quaternion and translation fields without checking direction

Answer: B. A name change does not transform coordinates. Use the measured frame relation and the intended target/source direction.

5. A local odometry estimate is continuous but drifts, while loop closure can correct global position abruptly. Which division of TF responsibilities fits that behavior?

- A. Global mapper owns map → odom; local estimator owns odom → base_link
- B. A rigid camera mount owns both moving transforms
- C. Publish odom → base_link as a static identity while the robot moves

Answer: A. REP 105 separates globally corrected positioning from continuous local odometry.

6. A dynamic transform tree exists, but a lookup fails for a replayed image’s timestamp. Which evidence should you inspect next?

- A. Only whether the frame names use underscores
- B. The requested time, buffer coverage and use_sim_time / replay clock configuration
- C. The app theme used during capture

Answer: B. Geometry must be available at the requested time. Wall-clock versus bag-clock mismatch can break an otherwise valid tree.

## A phone that helps build a map

1. A student installs the Android sensor APK and starts the TLS receiver on a laptop. Which pairing configuration identifies and authorizes that receiver?

- A. The reachable /ws/android WSS endpoint, exact server certificate SHA-256 and current session token
- B. An insecure ws:// endpoint containing only the app filename
- C. The APK download URL used as if it were the laptop receiver

Answer: A. The exact certificate pin identifies the TLS server, the token authorizes the session and the endpoint must be reachable over the chosen USB or Wi-Fi route.

2. An Android camera reports REALTIME and motion samples arrive, but camera–IMU extrinsics and noise have not been measured. What can you conclude about fusion readiness?

- A. The data is automatically ready for tightly coupled metric VIO
- B. The transport works, while estimator suitability and camera–IMU calibration remain unproven
- C. The camera’s metric depth is now available from each individual image

Answer: B. A shared phone clock and arriving samples are useful evidence. Inertial estimation still requires measured geometry, timing validation, uncertainty and a compatible integration stage.

3. The monocular ORB-SLAM3 viewer shows a sparse set of 3D landmarks after initialization. Which description is accurate for this course’s baseline?

- A. A dense, metrically scaled room mesh
- B. A sparse reconstruction with arbitrary scale and initially unqualified world orientation
- C. A saved navigation occupancy grid with guaranteed obstacle completeness

Answer: B. A calibrated monocular system estimates relative 3D structure and motion, while absolute scale remains unknown. Dense metric mapping needs additional information and processing.

4. The mapper does not initialize while the phone only rotates in place. Which change best supplies missing geometric information?

- A. Translate gently sideways through a textured, overlapping scene
- B. Raise the pairing token length to change map scale
- C. Rename image_raw to image_rect without processing pixels

Answer: A. Translation supplies parallax for monocular triangulation. Pure rotation does not establish feature depth.

5. After calibrating a fixed phone stream, the learner changes lens and image size. Which action is needed before trusting the mapping result?

- A. Keep using the old calibration because both lenses belong to one phone
- B. Restore the calibrated mode or recalibrate and regenerate matching settings
- C. Change only ROS_DOMAIN_ID to rescale the camera matrix

Answer: B. Intrinsics and image geometry depend on the actual lens/crop/resolution and processing mode.

6. The ROS adapter publishes tracked_points and a bounded path while Pangolin shows the engine’s map. Which evidence should a report distinguish?

- A. The ROS cloud/path are diagnostics, while the engine viewer shows its optimized sparse map
- B. Every received point is a permanently retained dense map vertex
- C. The path is automatically reoptimized whenever any loop closes

Answer: A. The supplied adapter exposes current tracked landmarks and historical poses. It does not claim a complete optimized ROS map export.

7. You replay a recorded phone run after stopping the live bridge. Which timing setup is appropriate for consumers of recorded sensor timestamps?

- A. Replay publishes /clock and relevant consumers use use_sim_time true
- B. Live bridge and replay publish the same topics concurrently to improve sample rate
- C. Use the laptop’s current wall time as if it were the original capture time

Answer: A. A single replay clock aligns consumers with recorded timestamps; competing live sources make interpretation ambiguous.
