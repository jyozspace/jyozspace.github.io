# The same graph, in C++

Change the language. Keep the communication contract.

## Translate the concepts

rclpy and rclcpp are client libraries for the same ROS graph. A Python subscriber can receive a C++ publisher's messages when name, type and QoS agree. C++ is useful for native libraries and demanding computation; Python is convenient for orchestration and experiments. Language choice alone does not make a system fast or real time.

Review classes, templates and smart pointers before class. If C++ is new, focus on mapping the familiar publisher, timer and callback concepts and use the complete reference scaffold. **By the end:** build a C++ node, connect it to Python and diagnose a QoS mismatch.

## Read a complete publisher

The supplied talker.cpp is the annotated version of this example:

```cpp
#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
using namespace std::chrono_literals;

class Talker : public rclcpp::Node {
public:
  Talker() : Node("cpp_talker") {
    pub_ = create_publisher<std_msgs::msg::String>("chatter", 10);
    timer_ = create_wall_timer(500ms, [this]() {
      std_msgs::msg::String msg;
      msg.data = "frame " + std::to_string(count_++);
      pub_->publish(msg);
    });
  }
private:
  int count_ = 0;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Talker>());
  rclcpp::shutdown();
  return 0;
}
```

The template argument sets the message type at compile time. SharedPtr members retain the publisher and timer. The lambda captures this to access members. `create_wall_timer` runs on steady time, independently of the ROS replay clock. During bag replay, use the node’s ROS clock when comparing sensor timestamps; this keeps measurements and time queries on the same timeline.

## Build and connect

For a talker, the essential CMake operations are:

```cmake
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
add_executable(talker src/talker.cpp)
ament_target_dependencies(talker rclcpp std_msgs)
install(TARGETS talker DESTINATION lib/${PROJECT_NAME})
ament_package()
```

This is an excerpt: the complete supplied CMakeLists.txt also defines the project, CMake version and other executables. package.xml declares dependencies for package discovery and dependency installation; CMake configures and links targets.

```bash
cd ~/ros2_ws
colcon build --packages-up-to ros2_course_cpp
source install/setup.bash
ros2 run ros2_course_cpp talker
```

In another terminal run `ros2 run ros2_course_py listener`. Expected: Python receives C++ strings. Reverse the pairing with the Python talker and C++ listener. Rebuild after a C++ edit; the old installed binary does not change automatically.

## Make QoS compatible

Quality of Service describes delivery and storage policies. **Reliable** requests retransmission when needed; it does not promise zero latency or delivery through every failure. **Best effort** permits loss, often favoring fresh sensor data over retries.

| Publisher offers | Subscriber requests | Compatible? |
| --- | --- | --- |
| Reliable | Reliable | Yes |
| Reliable | Best effort | Yes |
| Best effort | Reliable | No |
| Best effort | Best effort | Yes |

Compatibility is directional. Other policies matter too. Keep-last **depth** sets how many samples can be retained. When a consumer falls behind that finite history, older samples can be lost. **Durability** distinguishes volatile data from transient-local retained history. Late subscribers to retained map data or static transforms need suitable durability.

For sensors, inspect the publisher and often start with qos_profile_sensor_data in Python or rclcpp::SensorDataQoS() in C++. Inspect each driver’s offered policies before choosing the subscription profile.

## Break delivery, then repair it

Terminal A:

```bash
ros2 topic pub /qos_demo std_msgs/msg/String "{data: hello}" \
  --rate 2 --qos-reliability best_effort
```

Terminal B:

```bash
ros2 topic echo /qos_demo --qos-reliability reliable
```

Expected: no samples arrive; an incompatibility warning may appear. Stop echo, inspect the endpoints, then request best effort:

```bash
ros2 topic info /qos_demo --verbose
ros2 topic echo /qos_demo --qos-reliability best_effort
```

Expected: samples arrive. A subscriber policy fixed this pair; renaming the topic would not help. Predict all four reliability combinations in the interactive matrix.



![Simulated QoS checkpoint: inspect the best-effort offer, then select a compatible echo subscription.](../assets/qos-check.svg)

## Practice and prove it

**In class, 20 minutes:** connect C++ to Python, remap both endpoints and demonstrate the QoS failure. Submit verbose endpoint output and a one-sentence diagnosis.

**Homework, 45 minutes:** change the C++ talker to 5 Hz, rebuild and compare ros2 topic hz for Python and C++ talkers one at a time. This tiny example is not a valid language benchmark. Explain confounders such as logging, scheduling and subscriber overhead.

**Checkpoint:** reliable publisher to best-effort subscriber works. The reverse pair is incompatible. A queue depth is not a reliability policy.

Sources: [C++ tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html), [QoS compatibility](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html). Next: services, actions, launch and TF.
