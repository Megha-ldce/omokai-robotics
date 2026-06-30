#!/usr/bin/env python3
"""
Full pipeline: Prompt → LLM → Validated JSON → Executor
Groq runs in venv, executor runs with system Python (has ROS deps)
"""
import json
import sys
import os
import subprocess
from llm_planner import prompt_to_mission
from mission_validator import validate_and_report

def main():
    prompt = input("Enter mission prompt: ").strip()
    if not prompt:
        print("No prompt given.")
        sys.exit(1)

    print(f"\n[1/3] Sending to LLM...")
    mission = prompt_to_mission(prompt)
    print(json.dumps(mission, indent=2))

    print(f"\n[2/3] Validating mission...")
    validate_and_report(mission)

    mission_file = "/tmp/current_mission.json"
    with open(mission_file, "w") as f:
        json.dump(mission, f, indent=2)
    print(f"Mission saved to {mission_file}")

    print(f"\n[3/3] Executing mission...")
    # Use system python3 which has numpy, rclpy, nav2 msgs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    executor_path = os.path.join(script_dir, "mission_executor.py")
    subprocess.run(["/usr/bin/python3", executor_path, mission_file])

if __name__ == "__main__":
    main()