cmake_minimum_required(VERSION 3.8)
project(ros2_course_cpp)

# This course targets Jazzy and C++17.
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ---------------------------------------------------------------------------
# 1. FIND every dependency you use
# ---------------------------------------------------------------------------
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(ros2_course_interfaces REQUIRED)

# ---------------------------------------------------------------------------
# 2. For each executable: add_executable + ament_target_dependencies
# ---------------------------------------------------------------------------
add_executable(talker src/talker.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/listener.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

add_executable(area_server src/area_server.cpp)
ament_target_dependencies(area_server rclcpp ros2_course_interfaces)

add_executable(scan_min src/scan_min.cpp)
ament_target_dependencies(scan_min rclcpp sensor_msgs)

# ---------------------------------------------------------------------------
# 3. INSTALL them into lib/<package> so `ros2 run` can find them.
#    Forgetting this is the #1 reason for "No executable found".
# ---------------------------------------------------------------------------
install(TARGETS
  talker
  listener
  area_server
  scan_min
  DESTINATION lib/${PROJECT_NAME}
)

# If you later add launch/ or config/ folders to this package, install them too:
#   install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})

ament_package()
