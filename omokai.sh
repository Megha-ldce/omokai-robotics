#!/bin/bash
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=burger

echo "╔══════════════════════════════════════╗"
echo "║     OMOKAI ROBOTICS MISSION SIM      ║"
echo "╚══════════════════════════════════════╝"

echo "[1/3] Launching Gazebo..."
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py &
GAZEBO_PID=$!
sleep 10

echo "[2/3] Launching Nav2 + RViz..."
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  use_sim_time:=True \
  map:=/opt/ros/jazzy/share/turtlebot3_navigation2/map/map.yaml &
NAV2_PID=$!
sleep 8

echo "[3/3] Setting initial pose automatically..."
ros2 topic pub --once /initialpose geometry_msgs/msg/PoseWithCovarianceStamped '{
  header: {frame_id: "map"},
  pose: {
    pose: {
      position: {x: -2.0, y: -0.5, z: 0.0},
      orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
    },
    covariance: [0.25,0,0,0,0,0, 0,0.25,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0.068]
  }
}'

echo ""
echo "✅ All systems ready! Robot localized."
echo "   Run mission: omokai-mission"
echo ""
trap "echo 'Shutting down...'; kill $GAZEBO_PID $NAV2_PID 2>/dev/null; exit 0" SIGINT
wait