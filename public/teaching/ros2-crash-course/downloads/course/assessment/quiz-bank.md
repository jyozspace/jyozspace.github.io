# Course checkpoints

## Your robotics workbench

1. A learner is preparing a laptop for this course. Which environment matches the ROS 2 Jazzy installation commands?

- A. Ubuntu 24.04 with ROS 2 Jazzy
- B. Ubuntu 22.04 with the installation directory renamed
- C. Any Windows PowerShell tab without Ubuntu

Answer: A. The course uses Ubuntu Noble 24.04, Bash and Jazzy together. Windows learners run these commands inside Ubuntu under WSL 2.

2. wsl --version reports app version 3.x, while wsl -l -v lists Ubuntu-24.04 with VERSION 2. What should you do?

- A. Convert Ubuntu to VERSION 3
- B. Continue: the app version and Ubuntu engine version are different numbers
- C. Downgrade Ubuntu to VERSION 1

Answer: B. WSL app versions 2 or 3 are suitable here; Ubuntu must use the WSL 2 engine. The distro VERSION column should read 2.

3. Where should you keep the course workspace, and how can Windows Explorer open Linux home?

- A. Keep it in ~/ros2_ws; run cd ~ then explorer.exe . inside Ubuntu
- B. Keep it inside /opt/ros/jazzy and edit installed system files
- C. Store it inside WSL’s internal virtual disk by opening the disk file directly

Answer: A. Linux home is a suitable place for source and builds. explorer.exe . opens the current Linux directory through the supported WSL file-sharing path. Windows C: is available separately under /mnt/c.

4. A Linux ROS driver needs a USB sensor currently connected to Windows. What is the appropriate next route?

- A. Rename a topic to make the USB device appear
- B. Use usbipd-win to share and attach the selected device, then check Linux visibility and driver support
- C. Copy the device name into ~/ros2_ws/src

Answer: B. USB attachment and ROS communication are separate. usbipd-win exposes the selected device to WSL; Linux still needs a compatible driver and permissions. The Android ADB connection follows its own appendix.

5. The turtle window opens, but arrow keys do nothing while that window is focused. What should you try first?

- A. Focus the Ubuntu terminal running turtle_teleop_key and press arrows there
- B. Rebuild all four supplied packages before using turtlesim
- C. Run the Ubuntu commands in administrator PowerShell

Answer: A. The keyboard node reads keys in its own interactive terminal. Turtlesim is installed with the desktop tools and needs no course workspace build.

6. A fresh Ubuntu Bash terminal cannot find ros2 after installation. Which check is most useful?

- A. Inspect the saved .bashrc block and whether /opt/ros/jazzy/setup.bash is loaded
- B. Extract the course ZIP into Windows System32
- C. Change the phone camera calibration

Answer: A. ROS commands require the Jazzy underlay in that shell. The saved .bashrc block loads it for fresh interactive Bash terminals; the workspace overlay is available after the successful demo-package build later in lecture 00.

## From a robot to the ROS graph

1. A mobile robot measures a nearby obstacle and slows its wheels. Which explanation correctly connects sensing, processing and actuation?

- A. The distance sensor measures, a controller decides, and motor hardware changes motion
- B. The sensor alone chooses the route and directly becomes the operating system
- C. RViz supplies motor power whenever it displays a point cloud

Answer: A. Sensors provide observations, processing uses those observations and goals to choose commands, and actuators physically change the world; later observations close the feedback loop.

2. A student sees the name Robot Operating System and expects ROS 2 to replace Ubuntu. Where does ROS actually fit on this course laptop?

- A. It replaces the Linux kernel and BIOS
- B. Its libraries and tools run in user space above the operating system, supporting robotics applications
- C. It is a device firmware update installed directly onto every sensor

Answer: B. Ubuntu and its Linux kernel still manage processes, memory, devices and networking. ROS supplies application libraries, communication conventions and tools used by robotics programs.

3. A robot needs repeated camera frames, a short reset request and a cancellable drive-to-goal task. Which ROS interface selection fits these needs?

- A. A topic for images, a service for reset and an action for the longer task
- B. A parameter for every camera pixel and one service that never returns
- C. One unnamed shared file with no message types for all three interactions

Answer: A. Topics carry streams, services pair requests with responses, and actions add goal management, feedback, results and cancellation for longer operations. Parameters configure nodes.

4. In the basic command ros2 run turtlesim turtlesim_node, which parts select the package and the program that starts?

- A. turtlesim is the package; turtlesim_node is the executable
- B. turtlesim_node is the package; ros2 is the runtime node name
- C. Both words must be identical to the node name /turtlesim

Answer: A. ros2 run looks up an installed executable in a package. That program creates the runtime node /turtlesim; the executable name and node name can differ.

5. Two nodes appear in ros2 node list, but the turtle does not move. Which observation best establishes a correctly connected command stream?

- A. Both nodes use the same source language
- B. The publisher and subscriber resolve to the same topic/type with compatible QoS, and samples are observed
- C. Both programs were launched from the same directory

Answer: B. Process existence alone does not establish endpoint compatibility or data flow.

6. After starting ros2 run turtlesim turtlesim_node, which command shows the names of currently running ROS participants?

- A. ros2 node list
- B. ros2 topic list
- C. ros2 service list

Answer: A. ros2 node list inspects the running ROS graph. The topic and service list commands show communication interfaces; ros2 node list shows the current runtime node names.

7. A publisher is already running. What does ros2 topic echo /topic --once do when a matching sample arrives?

- A. It creates a subscriber, prints one sample and exits
- B. It rebuilds the publisher from its source files
- C. It starts every executable in the publisher package

Answer: A. The echo tool receives messages on a topic. With --once it finishes after one sample; it does not build code or launch the publisher.

8. You stop a velocity publisher with Ctrl+C while a physical base is moving. Which statement is appropriate before claiming the base is safely stopped?

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
