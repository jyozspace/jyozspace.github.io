cmake_minimum_required(VERSION 3.8)
project(ros2_course_bringup)

find_package(ament_cmake REQUIRED)

# A "bringup" package usually contains NO source code -- just launch files,
# parameter YAMLs and RViz configs that wire other packages together.
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
