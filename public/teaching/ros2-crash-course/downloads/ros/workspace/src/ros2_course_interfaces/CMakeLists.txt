cmake_minimum_required(VERSION 3.8)
project(ros2_course_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Every .msg / .srv / .action file must be listed here, or it will not be generated.
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  "srv/ComputeRectangleArea.srv"
  "action/CountUntil.action"
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
