// Lecture 5 - the same LaserScan processing as scan_stats.py, in C++.
//
// Run: ros2 run ros2_course_cpp scan_min --ros-args -p use_sim_time:=true
//
// Optional LiDAR example. Measure performance on your actual data;
// language choice alone is not a performance guarantee.

#include <algorithm>
#include <functional>
#include <cmath>
#include <limits>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

using std::placeholders::_1;

class ScanMin : public rclcpp::Node
{
public:
  ScanMin()
  : Node("cpp_scan_min")
  {
    // rclcpp::SensorDataQoS() is the C++ equivalent of qos_profile_sensor_data.
    subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
      "scan", rclcpp::SensorDataQoS(),
      std::bind(&ScanMin::callbackScan, this, _1));

    RCLCPP_INFO(this->get_logger(), "Waiting for /scan ...");
  }

private:
  void callbackScan(const sensor_msgs::msg::LaserScan::SharedPtr scan)
  {
    float closest = std::numeric_limits<float>::infinity();
    double closest_angle = 0.0;
    size_t valid = 0;

    for (size_t i = 0; i < scan->ranges.size(); ++i) {
      const float r = scan->ranges[i];
      if (!std::isfinite(r)) {continue;}
      if (r < scan->range_min || r > scan->range_max) {continue;}
      ++valid;
      if (r < closest) {
        closest = r;
        closest_angle = scan->angle_min + i * scan->angle_increment;
      }
    }

    if (valid == 0) {
      RCLCPP_WARN(this->get_logger(), "No valid returns in this scan.");
      return;
    }

    RCLCPP_INFO(
      this->get_logger(),
      "valid=%zu/%zu  closest=%.2f m at %.1f deg",
      valid, scan->ranges.size(), closest, closest_angle * 180.0 / std::acos(-1.0));
  }

  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ScanMin>());
  rclcpp::shutdown();
  return 0;
}
