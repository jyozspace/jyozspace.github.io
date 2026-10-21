# Annex D: explore more ROS workflows

Use these short experiments after the corresponding lecture. Each starts with the supplied packages and asks for evidence. Open one sourced terminal per long-running node. The capstone combines these skills; they are equally useful for a mobile robot, manipulator or sensor station.

## Services: inspect the contract, then implement a response

Start area_server, then inspect and call its interface in a second terminal:

```bash
ros2 run ros2_course_py area_server
```

```bash
ros2 interface show ros2_course_interfaces/srv/ComputeRectangleArea
ros2 service type /compute_area
ros2 service call /compute_area ros2_course_interfaces/srv/ComputeRectangleArea \
  "{width: 3.0, height: 4.0}"
```

Expect area 12.0, valid true and an explanatory message. Repeat with a negative width and explain the application’s rejection. Read area_server.py beside the .srv file: request fields arrive in the callback, response fields are assigned, and the callback returns that response. In area_client.py, trace call_async and the Future through which the result becomes available.

**Extend:** add a separate perimeter service using a new .srv interface, build its generated types and consumers, then test a valid rectangle and an invalid dimension. Give it its own service name. Follow the official [Python service/client tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html) for a full implementation pattern.

![Simulated service response and action feedback. The two interaction patterns expose different information to a client.](../assets/service-action.svg)

## Actions: trace goal, feedback, cancellation and result

Start count_until_server. In another terminal, inspect the action and send a goal:

```bash
ros2 interface show ros2_course_interfaces/action/CountUntil
ros2 action info /count_until
ros2 action send_goal /count_until ros2_course_interfaces/action/CountUntil \
  "{target: 8, period: 0.5}" --feedback
```

Observe goal acceptance, increasing current_number feedback and reached_number 8 in the result. Next use the supplied cancellation client:

```bash
ros2 run ros2_course_py count_until_client --ros-args \
  -p target:=20 -p period:=0.5 -p cancel_after:=2.0
```

Record the final status and number reached; timing can vary. Read count_until_server.py: goal validation, cancel handling and execute are distinct responsibilities. Its reentrant callback group and multithreaded executor let cancellation be processed while the teaching execute callback waits. For a sensor project, a “capture N frames” action could report progress and respond to a cancel request. Build that as an extension after tracing the supplied server. The [official action tutorial](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html) explains the server/client lifecycle.

## Bags: turn a live experiment into a repeatable input

With the phone streaming, record a short, consented scene. A ROS bag stores messages and their metadata, making later inspection and replay possible. MCAP is the usual default storage format in Jazzy; inspect the Storage id in your own output.

```bash
ros2 bag record -o ~/phone-lab/walk01 \
  /phone/camera/image_raw /phone/camera/camera_info \
  /phone/imu/accelerometer /phone/imu/gyroscope /phone/diagnostics
```

Stop the recorder with Ctrl+C so metadata is finalized. Run ros2 bag info and compare topic types, message counts and duration. Images may use substantial space, so start with a short run. Keep calibration files and a manifest beside the bag. Record physical TF topics too when your system has measured transforms that downstream consumers need.

![Simulated bag inspection and replay checklist. Actual counts, duration and storage format come from your recording.](../assets/bag-terminal.svg)

For replay, stop live publishers and restart relevant consumers with use_sim_time:=true. For example, append -p use_sim_time:=true to the optional mapper’s --ros-args parameters in lecture 5, keeping the same vocabulary and camera settings. Start a fresh engine so its internal map belongs to this run, then play:

```bash
ros2 bag play ~/phone-lab/walk01 --clock --rate 0.5
ros2 topic echo /clock --once
```

Run the echo in another terminal if play occupies yours. --clock publishes recorded ROS time; the rate option changes wall-time pacing. A slower run can reduce processing pressure while preserving recorded sensor timestamps. **Evidence:** compare tracking behavior on the same bag at normal and half speed and explain what changed. Follow the [official rosbag2 guide](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html) and [rosbag2 project](https://github.com/ros2/rosbag2/tree/jazzy) for storage, filtering and QoS overrides.

## TF: ask where a point was at its measurement time

Complete the Frames appendix’s demo_base/demo_sensor experiment. Use tf2_echo to inspect the transform and view_frames to inspect the tree. Calculate the transformed point before comparing with the interactive lesson. Explain who owns each edge and whether it should change over time.

![A metric mobile-robot frame chain and worked point transform. Phone monocular coordinates require a separate scale and alignment step.](../assets/tf-tree.svg)

Next read the [TF2 Python listener tutorial](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.html). A buffer stores transform history; a listener fills it. lookup_transform(target, source, time) retrieves the mapping from source into target. For sensor processing, request the measurement timestamp and handle missing data or extrapolation. A latest lookup is useful for inspection, but a moving system’s current pose can differ from its pose when the sample was acquired.

**Extend:** transform a PointStamped from demo_sensor into demo_base with tf2_geometry_msgs. Inspect its numeric coordinates and frame_id. This makes the distinction between relabeling a message and actually transforming it concrete.

## Parameters and launch: make runs repeatable

Change params_demo’s rate and text through ros2 param set, measure /chatter, then save the configuration:

```bash
ros2 param dump /params_demo > ~/phone-lab/params-demo.yaml
```

Stop the original node and restart with the saved configuration:

```bash
ros2 run ros2_course_py params_demo --ros-args \
  --params-file ~/phone-lab/params-demo.yaml
```

Compare accepted parameter values with observed output behavior. Then inspect pubsub_demo.launch.py: its launch arguments are explicitly passed to node parameters and remappings. Add a launch argument for your own experiment so runs can be configured from one repeatable command. Use the [launch tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html) and [parameter concepts](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html) to go further.

## Choose the next project by its missing contract

| Direction | What it adds | Official starting point |
| --- | --- | --- |
| Describe a robot | URDF links/joints and robot_state_publisher create a consistent frame model | [URDF tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html) |
| Start sensors in a controlled order | Lifecycle states make configure/activate/shutdown explicit | [Managed nodes design](https://design.ros2.org/articles/node_lifecycle.html) |
| Fuse metric sensors | Estimated uncertainty, frame semantics and timestamp consistency | [robot_localization](https://docs.ros.org/en/jazzy/p/robot_localization/) |
| Navigate a mobile robot | Metric localization, costmaps, planning and control | [Nav2 first-time setup](https://docs.nav2.org/setup_guides/index.html) |
| Simulate before hardware | A robot model and compatible ROS/Gazebo integration | [ROS/Gazebo compatibility](https://gazebosim.org/docs/latest/ros_installation/) |

Jazzy’s recommended modern Gazebo pairing is Harmonic. For each extension, write down the input topics, types, units, timestamps and transforms it expects. That habit turns a collection of working nodes into an understandable system.
