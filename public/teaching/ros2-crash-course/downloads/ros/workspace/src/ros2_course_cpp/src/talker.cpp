// Lecture 3 - the C++ (rclcpp) twin of the Python talker.
//
// Build: colcon build --packages-select ros2_course_cpp
// Run:   ros2 run ros2_course_cpp talker
//
// Compare this file line-by-line with ros2_course_py/talker.py. The CONCEPTS are
// identical; only the syntax changes.

#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;   // lets us write 500ms

class TalkerNode : public rclcpp::Node
{
public:
  TalkerNode()
  : Node("cpp_talker"), counter_(0)      // "cpp_talker" is the default node name
  {
    // Template argument = message type. Arguments = topic name, QoS depth.
    publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);

    timer_ = this->create_wall_timer(
      500ms,
      std::bind(&TalkerNode::publishMessage, this));

    RCLCPP_INFO(this->get_logger(), "C++ talker has been started.");
  }

private:
  void publishMessage()
  {
    auto msg = std_msgs::msg::String();
    msg.data = "Hello ROS 2 from C++! count = " + std::to_string(counter_);
    publisher_->publish(msg);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
    counter_++;
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int counter_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);                       // 1. start the client library
  auto node = std::make_shared<TalkerNode>();     // 2. create the node
  rclcpp::spin(node);                             // 3. process callbacks forever
  rclcpp::shutdown();                             // 4. clean up
  return 0;
}
