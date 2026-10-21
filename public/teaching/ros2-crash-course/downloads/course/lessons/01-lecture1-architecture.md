# Think in nodes and messages

A robot is a team of small programs. Learn to see the conversation.

## See the graph

ROS 2 (Robot Operating System 2) is a set of libraries, communication tools and conventions for robotic systems. It runs on an operating system; it does not replace Linux. A **node** has a focused job: reading a camera, estimating motion or responding to a command. One process can host one node or several composed nodes.

A **topic** is a named stream. Publishers send typed messages and subscriptions receive them through callbacks. A camera driver can publish frames while a viewer and an odometry node independently subscribe. The publisher does not directly call each subscriber. Endpoints need the same resolved topic name, compatible type and compatible QoS.

Most course traffic uses DDS through ROS's middleware abstraction. Discovery removes the need for a central ROS master. It does not guarantee reachability: network isolation, multicast, domains and endpoint policies can still stop delivery.

**By the end:** inspect a graph, explain what a topic carries, send a command and diagnose a silent subscriber. These same skills will debug camera streams in lecture 5.

## Bring a turtle to life

Terminal A, with Jazzy sourced:

```bash
ros2 run turtlesim turtlesim_node
```

Terminal B, also sourced:

```bash
ros2 run turtlesim turtle_teleop_key
```

Keep terminal B focused and press the arrow keys. Expected: the turtle moves in its window. Keyboard commands reach the simulator through `/turtle1/cmd_vel`.

Run turtle_teleop_key in an interactive Ubuntu terminal. A piped command, background task or automation without a TTY can abort with `Failed to get old console mode`. Reopen it in a normal Ubuntu terminal; use topic pub below for scripted motion checks.

In terminal C:

```bash
ros2 node list
ros2 node info /turtlesim
ros2 topic list -t
ros2 topic info /turtle1/cmd_vel --verbose
ros2 topic echo /turtle1/pose --once
rqt_graph
```

Expected: `/turtlesim` and `/teleop_turtle` appear. Pose contains x, y, theta and velocities. Infrastructure topics may appear too; rqt_graph filters can hide unused endpoints. Use the topic name and message type to match this graph to your own output.

![Simulated turtlesim and graph view: the keyboard controller publishes Twist to the simulator through cmd_vel.](../assets/turtle-graph.svg)


## Read an interface

```bash
ros2 interface show geometry_msgs/msg/Twist
ros2 interface show turtlesim/msg/Pose
ros2 topic hz /turtle1/pose
```

Twist contains linear and angular Vector3 fields. For the 2D turtle, linear.x drives forward and angular.z turns. Physical robots typically interpret these as metres per second and radians per second. Turtlesim screen coordinates are simulation units, with coordinates defined by the simulator.

Stop the keyboard controller before adding another command publisher:

```bash
ros2 topic pub --rate 2 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.5}}"
```

Expected: a circle. Press Ctrl+C, then send a zero command:

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

A zero command is a software request, not an emergency stop. A physical base needs motion limits, a command watchdog and an independent stop. Stopping a publisher alone need not stop its consumer.

## Reconnect without editing code

`chatter` is relative; `/chatter` is absolute. Namespaces group interfaces, while remapping changes connections at runtime. Start another simulator:

```bash
ros2 run turtlesim turtlesim_node --ros-args -r __ns:=/robot2
```

Expected: `/robot2/turtlesim` and `/robot2/turtle1/pose`. A namespace changes graph names. It does not automatically change physical coordinate frames or securely isolate traffic.

Camera connection: launch remappings can connect `/phone/camera/image_raw` to an estimator's input. Inspect the actual stream first. Renaming an image does not rectify pixels or repair calibration.

## Debug from the outside in

1. Check that the intended process is still running and its terminal has no error.
2. Run node list and topic list in a terminal with the same ROS environment.
3. Use topic info with --verbose: inspect endpoints, type and QoS.
4. Echo one sample; select best effort for a best-effort sensor if needed.
5. Check domain, discovery and network reachability before editing application code.

`ros2 topic hz` measures the samples received by that tool. It is not a precise hardware frequency or end-to-end latency measurement. Topic discovery alone is not proof that useful data arrives.

Deliberately remap the keyboard node's command topic to `/wrong_cmd_vel`. Predict the disconnected graph, test it and repair the remap. Stop that node before restarting the correct teleop.

Read more: the official [nodes guide](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html) shows additional node introspection commands, while the [topics guide](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html) explains echo, rate and interface inspection.

## Practice and prove it

**In class, 20 minutes:** drive a circle, inspect Twist and start a second namespaced turtle. Submit the topic names and explain which publisher can move which turtle. Success means the explanation matches the graph.

**Homework, 30 minutes:** publish a straight segment and a turn, send zero velocity and draw the command and pose connections. Record which terminal runs each node and save the CLI evidence.

**Checkpoint:** a publisher and subscriber agree on name and type but exchange no samples. Inspect endpoint QoS, then environment and transport. The name is only part of the contract.

Source: [ROS 2 beginner CLI tutorials](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools.html). Next: create your own publisher and subscriber in Python.
