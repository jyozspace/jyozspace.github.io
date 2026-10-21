# Connect a complete system

Choose the right interaction. Give every measurement a place and a time.

## Choose topics, services or actions

Use a **topic** for a continuing stream, such as camera frames. Use a **service** for a short request and response, such as reading a setting or computing an area. Use an **action** for a longer goal that needs feedback and cancellation, such as navigating to a pose.

A service client sends a request and waits for a response from a server. If a connection fails, retrying may repeat work, so operations such as saving a file need an application-level retry policy. Keep service callbacks short so other work can be processed. An action adds goal acceptance, feedback and a final status; its server also needs to check and respond to cancellation requests.

**By the end:** call a custom service, send an action goal, configure nodes through parameters and launch, and explain a TF chain. This lecture is dense: the core path is CLI use plus the supplied files; implementing a new action server is an extension.

## Call a service

The supplied ComputeRectangleArea.srv has request fields above the separator and response fields below:

```text
float64 width
float64 height
---
float64 area
bool valid
string message
```

Start the Python server:

```bash
ros2 run ros2_course_py area_server
```

In a second terminal:

```bash
ros2 service list -t
ros2 service call /compute_area \
  ros2_course_interfaces/srv/ComputeRectangleArea \
  "{width: 3.0, height: 4.0}"
ros2 run ros2_course_py area_client --ros-args -p width:=5.0 -p height:=2.5
```

Expected: valid true with area 12.0 for the CLI call and 12.5 for the client. Negative or non-finite dimensions should be rejected by the application. Run one server at a time: two servers advertising the same service make it unclear which implementation handled a request.

Read area_client.py: call_async returns a Future, and an executor must keep processing work for the response to arrive. The standalone client can spin while waiting. Inside an already-spinning node callback, use an asynchronous continuation and suitable callback groups instead: blocking that callback can prevent its own response from being processed.

## Follow a goal over time

CountUntil.action separates goal, result and feedback with two separators:

```text
int32 target
float64 period
---
int32 reached_number
---
int32 current_number
```

Run the server, then send a goal in another terminal:

```bash
ros2 run ros2_course_py count_until_server
```

```bash
ros2 action list -t
ros2 action send_goal /count_until \
  ros2_course_interfaces/action/CountUntil \
  "{target: 8, period: 0.5}" --feedback
```

Expected: feedback counts upward and the result reports reached_number 8. The server rejects nonpositive targets and invalid periods. Its teaching implementation uses a multithreaded executor and a reentrant callback group, so cancellation can be serviced while execution waits. It is not a real-time job scheduler.

To demonstrate cancellation, run `ros2 run ros2_course_py count_until_client --ros-args -p target:=20 -p period:=0.5 -p cancel_after:=2.0`. The client requests cancellation after two seconds and logs the terminal status. Cancellation is a protocol: Ctrl+C on an arbitrary CLI client does not by itself guarantee that the server cancels the goal.



![Simulated service response and action feedback. An action exposes progress and a terminal goal state.](../assets/service-action.svg)

For a deeper source walkthrough, try [Annex D’s service and action experiments](../annexes/ros-workflows.md).

## Configure and launch

Parameters configure a node. Declare them with defaults, validate values and make the runtime behavior match accepted updates. A parameter changing in the graph does not automatically rebuild a timer or reconfigure a sensor.

```bash
ros2 run ros2_course_py params_demo --ros-args -p rate_hz:=2.0
```

In another terminal:

```bash
ros2 param list /params_demo
ros2 param set /params_demo message "changed live"
ros2 param set /params_demo rate_hz 5.0
ros2 topic hz /chatter
```

Expected: new messages use the new text and the output rate changes to about 5 Hz. The reference implementation validates positive finite rates and reads committed parameters and replaces its timer at the next existing timer tick. Stop this node before the next demonstration.

Launch files are repeatable system recipes. They configure nodes, remappings and parameters, but textual order alone does not guarantee a dependency is ready. For more complex systems use lifecycle management or explicit readiness checks.

```bash
ros2 launch ros2_course_py pubsub_demo.launch.py \
  message:="camera pipeline ready" rate:=5.0
```

Expected: my_talker and my_listener exchange messages on /lecture_chatter. A launch argument is an input to the launch description; a parameter belongs to a node. The launch file explicitly passes one into the other.

## Give data a coordinate frame

An image has a timestamp and frame_id in its Header. TF2 answers how coordinate frames relate at a requested time. The standard mobile-robot chain is `map → odom → base_link → camera_link → camera_optical_frame`.

**map → odom:** a mapping/localization estimate corrects global drift and can jump after loop closure. **odom → base_link:** local odometry is continuous but can drift. **base_link → sensor:** a calibrated rigid mount is static. Exactly one authority should publish each child frame's parent transform.

REP 103 uses x forward, y left and z up for a body frame. Optical frames use x right, y down and z forward. A frame name alone does not rotate the data. Use measured geometry for physical sensors. A static transform describes a rigid mount; a moving sensor’s pose needs a changing estimate.

Try a deliberately simple fixed-frame exercise. These values describe a teaching mount, not your hardware calibration:

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 0.1 --y 0.0 --z 0.2 --yaw 0 --pitch 0 --roll 0 \
  --frame-id base_link --child-frame-id camera_link
```

In another terminal:

```bash
ros2 run tf2_ros tf2_echo base_link camera_link
ros2 run tf2_tools view_frames
```

Expected: the translation is 0.1, 0, 0.2 metres. view_frames writes a graph file in the working directory. A lookup outside the buffer's time range can fail even when every frame name exists. Inspect timestamps, clock and transform availability together.



![Frame ownership and a worked transform. This metric mobile-robot example is separate from the arbitrary-scale phone world.](../assets/tf-tree.svg)

## Work through one point transform

Suppose demo_sensor is translated by (0.1, 0, 0.2) m in demo_base and yawed +90° around z. Its point (1, 0, 0) m becomes (0, 1, 0) after rotation, then (0.1, 1.0, 0.2) after translation. This is different from changing frame_id: the numbers must change too.

Use the interactive transform lab, then read the Frames appendix. A lookup_transform(target, source, time) returns the transform mapping source coordinates into target coordinates at that time. Optical axes, body axes and phone-device axes use separate conventions. The phone camera–IMU mounting becomes an edge in this tree only after its geometry and axis conventions have been measured.

## Practice and prove it

**In class, 25 minutes:** launch the pub/sub pair, update a validated parameter and produce the fixed TF above. Submit the launch command, measured rate and frame graph. Stop the teaching static transform before starting a real sensor driver that publishes the same child frame.

**Homework, 60 minutes:** sketch the future camera system. Label topic types, clock source and the node responsible for each TF edge. Explain why a static odom → base_link would claim a moving rig is stationary.

**Checkpoint:** a map correction may jump, while local odometry should remain continuous. That is why the global and local transforms are split.

Sources: [services](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html), [actions](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html), [REP 103](https://www.ros.org/reps/rep-0103.html), [REP 105](https://www.ros.org/reps/rep-0105.html). Read the Frames, transforms & time appendix for worked point transforms, composition, quaternions and lookup direction. Next: connect phone sensors and qualified monocular SLAM.
