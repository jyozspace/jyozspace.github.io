# Write your first Python nodes

Turn the graph into code, one callback at a time.

## Understand the workspace

A **workspace** contains source packages and generated build, install and log directories. A **package** groups code, interfaces and metadata. An **executable** is a runnable entry point; a **node** participates in the graph. These are related concepts, not synonyms.

The reference workspace contains ros2_course_py, ros2_course_cpp, ros2_course_interfaces and ros2_course_bringup. Use it to catch up, but type this first experiment yourself. **By the end:** write timer and subscription callbacks, build a package and explain interface generation.

## Write a complete publisher

Save this as `~/ros2_ws/hello.py`. With Jazzy sourced, run `python3 ~/ros2_ws/hello.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Hello(Node):
    def __init__(self):
        super().__init__('hello')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.count = 0
        self.timer = self.create_timer(0.5, self.tick)

    def tick(self):
        msg = String()
        msg.data = f'frame {self.count}'
        self.publisher.publish(msg)
        self.count += 1

def main():
    rclpy.init()
    node = Hello()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Node gives the object a graph identity. A **callback** is a function ROS invokes when work is ready, such as a timer expiring or a message arriving. The **executor** chooses and runs ready callbacks while `spin` is active. The publisher specifies String and keep-last depth 10 using the default profile. The timer requests a callback roughly twice per second; scheduling can vary on an ordinary laptop.

In another terminal, `ros2 topic echo /chatter` should show frame 0, frame 1 and increasing counts. Keep callbacks short: a long sleep or expensive computation in a single-threaded callback delays other callbacks on that executor.

## Install a package entry point

Create a scratch package. The package name comes before --dependencies so it cannot be consumed as a dependency:

```bash
cd ~/ros2_ws/src
ros2 pkg create my_camera_lab --build-type ament_python \
  --license Apache-2.0 --dependencies rclpy std_msgs
```

Copy hello.py into `my_camera_lab/my_camera_lab/hello.py`. Add `'hello = my_camera_lab.hello:main'` to the console_scripts list in setup.py. package.xml declares dependencies and setup.cfg places scripts where ros2 run expects them.

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_camera_lab
source install/setup.bash
ros2 run my_camera_lab hello
```

Expected: the same /hello node and /chatter stream. If the executable is absent, check the entry point, rebuild and source the overlay in a fresh terminal. Stop the scratch publisher before starting the reference talker.

## Receive messages

Run the supplied reference pair in separate sourced terminals:

```bash
ros2 run ros2_course_py talker
```

```bash
ros2 run ros2_course_py listener
```

The listener should log the talker's strings. Resources includes both complete source files. `create_subscription(String, 'chatter', callback, 10)` connects incoming messages to a function accepting a message argument. Store the subscription on the node object so its ownership is clear.

Change the listener to log `len(msg.data)`. Then remap both nodes using `--ros-args -r chatter:=camera_events`. Remapping only one node disconnects them. Stop duplicate publishers when measuring rates.

Large image processing needs deliberate design. Copying every frame through many callbacks can consume CPU and bandwidth. Measure your pipeline before choosing an optimization or a language.

## Write the matching minimal subscriber

Save as ~/ros2_ws/hear.py and run with Jazzy sourced while hello.py is publishing. This complete scaffold uses the same type, relative name and QoS depth as the publisher:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Hear(Node):
    def __init__(self):
        super().__init__('hear')
        self.sub = self.create_subscription(String, 'chatter', self.receive, 10)

    def receive(self, msg):
        self.get_logger().info(f'Received {len(msg.data)} characters: {msg.data}')

def main():
    rclpy.init()
    node = Hear()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Expected: a line for each received frame string. The callback handles one message; spin lets the executor invoke it. Stop the scratch pair before starting another talker. In the package version, install Hear through a console_scripts entry point just as you did for Hello.

## Give data a meaningful type

String is convenient for a first lesson. Real interfaces should describe their data: Image for pixels, CameraInfo for calibration and Imu for inertial measurements. Our custom RobotStatus demonstrates generation:

```text
string robot_name
float32 battery_percent
bool is_moving
uint8 fault_code
```

ros2_course_interfaces lists files in rosidl_generate_interfaces in CMakeLists.txt and declares generator/runtime dependencies in package.xml. Interfaces live in an ament_cmake package even when consumers are Python. Build before importing generated types:

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-up-to ros2_course_py
source install/setup.bash
ros2 interface show ros2_course_interfaces/msg/RobotStatus
ros2 run ros2_course_py robot_status_publisher
```

In another terminal, `ros2 topic echo /robot_status --once` should show the fields. This example simulates battery state; it does not measure a real battery. Document units, valid ranges and unavailable values. Use a Header when timestamp and coordinate frame matter.



![Simulated installed talker and listener terminals. Compare their resolved topic, type and increasing message values.](../assets/pubsub-terminal.svg)

## Practice and prove it

**In class, 25 minutes:** write a subscriber that counts received messages and reports once per second. Increment a counter in its subscription callback and report it in a timer callback. At a 2 Hz input the count usually grows by about two per report after startup. Asynchronous interval boundaries mean it need not be exactly two every time.

**Homework, 45 minutes:** add float32 temperature_c to RobotStatus, regenerate the interface, rebuild consumers and publish a simulated value. Submit the interface, changed publisher and one echoed message.

**Checkpoint:** editing a .msg file does not generate an importable type. Build the interface package and dependent consumers, then source the overlay.

Sources: [Python publisher/subscriber](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [custom interfaces](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html). Next: connect Python and C++ and diagnose QoS.
