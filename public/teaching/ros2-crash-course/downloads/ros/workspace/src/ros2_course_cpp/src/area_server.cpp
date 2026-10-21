// Lecture 3/4 - a C++ service server using our custom interface.
//
// Run:  ros2 run ros2_course_cpp area_server
// Call: ros2 service call /compute_area \
//         ros2_course_interfaces/srv/ComputeRectangleArea "{width: 3.0, height: 4.0}"

#include <cmath>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "ros2_course_interfaces/srv/compute_rectangle_area.hpp"
//                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^
// NOTE the naming rule: the interface file ComputeRectangleArea.srv becomes the
// header compute_rectangle_area.hpp (CamelCase -> snake_case).

using ComputeRectangleArea = ros2_course_interfaces::srv::ComputeRectangleArea;
using std::placeholders::_1;
using std::placeholders::_2;

class AreaServer : public rclcpp::Node
{
public:
  AreaServer()
  : Node("cpp_area_server")
  {
    server_ = this->create_service<ComputeRectangleArea>(
      "compute_area",
      std::bind(&AreaServer::callbackComputeArea, this, _1, _2));

    RCLCPP_INFO(this->get_logger(), "C++ area service is ready.");
  }

private:
  void callbackComputeArea(
    const ComputeRectangleArea::Request::SharedPtr request,
    const ComputeRectangleArea::Response::SharedPtr response)
  {
    if (!std::isfinite(request->width) || !std::isfinite(request->height) ||
      request->width < 0.0 || request->height < 0.0 ||
      !std::isfinite(request->width * request->height)) {
      response->area = 0.0;
      response->valid = false;
      response->message = "dimensions and area must be finite; dimensions must be >= 0";
    } else {
      response->area = request->width * request->height;
      response->valid = true;
      response->message = "ok";
    }

    RCLCPP_INFO(
      this->get_logger(), "%.2f x %.2f -> %.2f",
      request->width, request->height, response->area);
  }

  rclcpp::Service<ComputeRectangleArea>::SharedPtr server_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AreaServer>());
  rclcpp::shutdown();
  return 0;
}
