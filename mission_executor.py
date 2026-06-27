#!/usr/bin/env python3
import json
import sys
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus

class MissionExecutor(Node):
    def __init__(self):
        super().__init__('mission_executor')
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.get_logger().info('Mission Executor ready.')

    def execute_mission(self, mission):
        mission_name = mission["mission_name"]
        repeat = mission["repeat"]
        waypoints = mission["waypoints"]
        self.get_logger().info(f"Mission: {mission_name} | {len(waypoints)} waypoints | repeat={repeat}")

        if not self._client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Nav2 not available!')
            return False

        for run in range(repeat):
            self.get_logger().info(f"--- Run {run+1}/{repeat} ---")
            for i, wp in enumerate(waypoints):
                label = wp.get("label", f"WP{i}")
                self.get_logger().info(f"Going to {label} ({wp['x']:.2f}, {wp['y']:.2f})")
                if not self._go_to_waypoint(wp["x"], wp["y"]):
                    self.get_logger().error(f"Failed at {label}. Aborting.")
                    return False
                self.get_logger().info(f"Reached {label} ✅")

        self.get_logger().info(f"Mission complete ✅")
        return True

    def _go_to_waypoint(self, x, y):
        goal = NavigateToPose.Goal()
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        pose.pose.orientation.w = 1.0
        goal.pose = pose

        future = self._client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected!')
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        return result_future.result().status == GoalStatus.STATUS_SUCCEEDED

def main():
    print("[EXECUTOR] Starting...", flush=True)
    if len(sys.argv) < 2:
        print("Usage: python3 mission_executor.py <mission.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        mission = json.load(f)

    print("[EXECUTOR] Initializing ROS...", flush=True)
    rclpy.init()
    print("[EXECUTOR] ROS ready.", flush=True)
    node = MissionExecutor()
    success = node.execute_mission(mission)
    node.destroy_node()
    rclpy.shutdown()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
