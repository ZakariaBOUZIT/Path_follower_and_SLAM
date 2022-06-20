cmake_minimum_required(VERSION 3.0.2)
project(turtlebot_path_following)

find_package(
catkin REQUIRED COMPONENTS
geometry_msgs
turtlesim
)


catkin_package(
  CATKIN_DEPENDS
  geometry_msgs
  turtlesim
)

