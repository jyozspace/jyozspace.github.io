# Visual checkpoints: what should I see?

Use this gallery when you are unsure what a command or tool is meant to reveal. Each software view is a **simulated teaching example**, with illustrative values and simplified layout. Compare the named fields and relationships with your own output. Open a picture for full resolution. The figures also appear next to the corresponding course steps.

## Setup and the graph

Check ROS_DISTRO and Ubuntu codename first. After the workspace builds, verify that executables are installed and visible in the current sourced terminal.

![Simulated setup terminal. Jazzy, noble, four packages and a visible executable list are the checkpoints.](../assets/setup-terminal.svg)

Drive the turtle with the teleop terminal focused. A moving turtle shows behavior; the graph explains the publisher, topic and subscriber behind it.

![Simulated turtlesim and command graph. The typed cmd_vel stream links the keyboard controller to the simulator.](../assets/turtle-graph.svg)

## Programs and interaction patterns

Keep the publisher and listener running in separate terminals. Increasing message values and a shared topic show data flow. The logger prefix identifies the node that printed the line.

![Simulated pub/sub terminals. One installed talker publishes strings while the listener receives them.](../assets/pubsub-terminal.svg)

![Simulated QoS diagnosis. A best-effort publisher needs a subscriber whose reliability request it can meet.](../assets/qos-check.svg)

![Simulated service and action outputs. Compare a single response with feedback and a final goal result.](../assets/service-action.svg)

## Frames and sensor transport

The metric mobile-robot chain teaches transform ownership. The phone’s monocular world is a separate arbitrary-scale visualization frame.

![Frame ownership diagram and worked transform. Rotation followed by translation changes the point coordinates.](../assets/tf-tree.svg)

![Native phone pipeline. Camera2 and independently timestamped motion events reach the laptop receiver.](../assets/native-pipeline.svg)

![Simulated Android pairing checkpoint. Inspect the camera mode, clock source and separate component counters.](../assets/android-screen.svg)



![Simulated image_view and received topic rate. Compare your own camera scene, dimensions and observed rate.](../assets/image-view.svg)

## Calibration, timing and mapping

Use measured target dimensions and varied camera views. Timing exchanges estimate the phone-to-laptop clock relation. Inspect the native camera’s timestamp source and measure camera–IMU alignment separately.

![Simulated checkerboard tool. Track horizontal, vertical, size and skew coverage before fitting and saving.](../assets/calibration-screen.svg)

![IMU inspection guide. Test rest values and single-axis turns before planning sensor fusion.](../assets/imu-check.svg)

![Clock conversion timeline. Inspect capture timing separately from the estimated phone-to-laptop clock relation.](../assets/clock-timeline.svg)

![Simulated sparse-map display. Sparse landmarks and a diagnostic path provide structure with arbitrary scale.](../assets/sparse-map.svg)

## USB and wireless connection routes

![Android connection options. ADB reverse carries USB packets; the phone hotspot carries wireless packets to the same receiver.](../assets/android-connections.svg)

### WSL connection route

![WSL USB route. Android localhost reaches the receiver inside Ubuntu through Windows ADB and localhost forwarding.](../assets/wsl-route.svg)

## Recording and reproducibility

Inspect the recording’s actual topic counts, storage format and duration. Stop live publishers, then use the replay clock consistently in consumers.

![Simulated bag information and playback. Use matching camera settings and a fresh mapper process for the recorded run.](../assets/bag-terminal.svg)

For a lab report, replace these examples with your own screenshots and the commands that produced them. Record what a viewer establishes: transport, image quality, tracking state and reconstruction are distinct observations.
