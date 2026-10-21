// Lecture 3 - the C++ subscriber.
//
// Run:  ros2 run ros2_course_cpp listener
//
// Cross-language check: run the PYTHON talker and the C++ listener together.
// They interoperate, because both speak DDS on the wire, not Python or C++.

#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;

class ListenerNode : public rclcpp::Node
{
public:
  ListenerNode()
  : Node("cpp_listener")
  {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "chatter", 10,
      std::bind(&ListenerNode::callbackChatter, this, _1));

    RCLCPP_INFO(this->get_logger(), "C++ listener started, waiting...");
  }

private:
  void callbackChatter(const std_msgs::msg::String::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ListenerNode>());
  rclcpp::shutdown();
  return 0;
}
