# Sources and Citations

All sources used in building this project.

---

## Core Frameworks (used as runtime dependencies, not copied)

| Source | URL | License | What I used |
|---|---|---|---|
| ROS 2 Jazzy | https://github.com/ros2/ros2 | Apache 2.0 | DDS middleware, rclpy, action client API |
| Nav2 | https://github.com/ros-navigation/navigation2 | Apache 2.0 | NavigateToPose action, lifecycle manager, AMCL localization |
| TurtleBot3 | https://github.com/ROBOTIS-GIT/turtlebot3 | Apache 2.0 | Robot URDF, Gazebo sim, pre-built map, Nav2 launch files |
| TurtleBot3 Simulations | https://github.com/ROBOTIS-GIT/turtlebot3_simulations | Apache 2.0 | Gazebo world, spawn configuration |
| Gazebo Harmonic | https://github.com/gazebosim/gz-sim | Apache 2.0 | Physics simulation |

## LLM / API

| Source | URL | License | What I used |
|---|---|---|---|
| Groq API | https://console.groq.com | Proprietary (free tier) | LLM inference — Llama-3.3-70B-Versatile for prompt-to-JSON |
| Groq Python SDK | https://github.com/groq/groq-python | Apache 2.0 | Python client for API calls |
| Meta Llama 3.3 70B | https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct | Llama 3.3 Community License | Model weights (served via Groq, not self-hosted) |

## Reference Repos (architecture inspiration, no code copied)

| Source | URL | License | What I referenced |
|---|---|---|---|
| ChatDrones | https://github.com/Gaurang-1402/ChatDrones | MIT | NL→structured JSON command pattern for ROS 2 |
| ROS-LLM | https://github.com/Auromix/ROS-LLM | Apache 2.0 | General NL-control framework architecture reference |
| Nav2 Simple Commander | https://github.com/ros-navigation/navigation2/tree/main/nav2_simple_commander | Apache 2.0 | NavigateToPose usage pattern reference |

## Python Libraries

| Package | Version | License | Purpose |
|---|---|---|---|
| groq | 1.5.0 | Apache 2.0 | Groq API client |
| pyyaml | 6.0.3 | MIT | YAML parsing (required by rclpy) |
| pydantic | 2.13.4 | MIT | Data validation (groq dependency) |

## Documentation Referenced

- ROS 2 Jazzy Action Client tutorial: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html
- Nav2 Python API docs: https://docs.nav2.org/commander_api/index.html
- TurtleBot3 simulation guide: https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/
- Groq API reference: https://console.groq.com/docs/openai

---

## AI Assistance Disclosure

This project was developed with AI assistance (Claude by Anthropic) for:
- Code scaffolding and debugging
- Troubleshooting ROS 2 TF frame issues
- File writing assistance

All code has been reviewed, understood, and tested by the author.
The architecture decisions, system design, and debugging were done collaboratively.
The author can explain every line of code and make modifications independently.
