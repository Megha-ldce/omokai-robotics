# Omokai Robotics — LLM-Controlled Ground Robot

A pipeline that converts natural language prompts into validated robot missions, executed deterministically in simulation.

```
Prompt → LLM (Groq/Llama-3.3-70B) → Validated Mission JSON → Deterministic Executor → TurtleBot3 (Gazebo + Nav2)
```

---

## Architecture

| Stage | File | Role |
|---|---|---|
| Prompt | CLI input | Natural language from operator |
| LLM | `llm_planner.py` | Groq API (Llama-3.3-70B) interprets intent, emits structured JSON |
| Validator | `mission_validator.py` | Schema + safety checks before anything executes |
| Executor | `mission_executor.py` | Deterministic: same JSON → same behaviour, always. LLM never in control loop |
| Simulator | Gazebo + Nav2 | TurtleBot3 burger follows Nav2 NavigateToPose goals |

### Key Design Decisions
- **LLM is kept out of the control loop.** It only produces a plan. The executor reads validated JSON — it has no LLM dependency.
- **Validation is a hard gate.** If speed > 0.5 m/s, coordinates > 20m, or schema is wrong, the mission is rejected before the robot moves.
- **Deterministic executor.** The same JSON file always produces the same robot behaviour. Auditable and testable independently of the LLM.

---

## Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic (comes with Jazzy)
- Python 3.12
- Internet connection (for Groq API)
- Groq API key (free at console.groq.com — no credit card required)

---

## Installation

### Option A: Docker (recommended for portability)

```bash
git clone https://github.com/YOUR_USERNAME/omokai-robotics.git
cd omokai-robotics
docker build -t omokai .
xhost +local:docker
docker run -it --rm \
  --env DISPLAY=$DISPLAY \
  --env GROQ_API_KEY=your_key_here \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --network host \
  omokai
```

### Option B: Native install on Ubuntu 24.04

```bash
# 1. Install ROS 2 Jazzy (if not already installed)
# https://docs.ros.org/en/jazzy/Installation.html

# 2. Install TurtleBot3 and Nav2
sudo apt install -y \
  ros-jazzy-turtlebot3 \
  ros-jazzy-turtlebot3-simulations \
  ros-jazzy-turtlebot3-gazebo \
  ros-jazzy-turtlebot3-navigation2 \
  python3.12-venv

# 3. Clone and set up
git clone https://github.com/YOUR_USERNAME/omokai-robotics.git
cd omokai-robotics
python3 -m venv venv
source venv/bin/activate
pip install groq pyyaml

# 4. Set your Groq API key
export GROQ_API_KEY=your_key_here
# Or edit llm_planner.py and replace the GROQ_API_KEY value

# 5. Add aliases
echo "alias omokai='~/omokai-robotics/omokai.sh'" >> ~/.bashrc
echo "alias omokai-mission='cd ~/omokai-robotics && source venv/bin/activate && source /opt/ros/jazzy/setup.bash && python3 run_mission.py'" >> ~/.bashrc
source ~/.bashrc
```

---

## How to Run

### Step 1 — Launch simulation (Terminal 1)
```bash
omokai
```
Wait for the message: `✅ All systems ready! Robot localized.`

This launches:
- Gazebo with TurtleBot3 world
- Nav2 navigation stack with pre-built map
- Automatic initial pose estimation (no manual RViz click needed)

### Step 2 — Send a mission prompt (Terminal 2)
```bash
omokai-mission
```

Type any natural language command, for example:
```
Drive a 2 metre square loop
Patrol the perimeter twice at slow speed
Go forward 3 metres and return to start
Drive a 3 metre triangle
Move in an L-shape covering 2 metres each side
```

### What to expect
1. The LLM generates a mission JSON with waypoints
2. The validator checks speed limits, coordinate bounds, schema
3. If valid, the executor sends Nav2 goals one by one
4. The robot moves in both Gazebo and RViz
5. Each waypoint reached is logged with ✅

---

## Example Session

```
$ omokai-mission
Enter mission prompt: Patrol the perimeter twice at slow speed

[1/3] Sending to LLM...
{
  "mission_name": "Perimeter Patrol",
  "repeat": 2,
  "speed": 0.05,
  "waypoints": [
    {"x": -2.0, "y": -0.5, "label": "Start"},
    {"x": 0.0,  "y": -0.5, "label": "East"},
    {"x": 0.0,  "y":  1.5, "label": "North-East"},
    {"x": -2.0, "y":  1.5, "label": "North"},
    {"x": -2.0, "y": -0.5, "label": "Return"}
  ]
}

[2/3] Validating mission...
[VALIDATOR] ✅ Mission 'Perimeter Patrol' passed all checks.

[3/3] Executing mission...
[INFO] Mission: Perimeter Patrol | 5 waypoints | repeat=2
[INFO] --- Run 1/2 ---
[INFO] Going to Start (-2.00, -0.50)
[INFO] Reached Start ✅
...
[INFO] Mission complete ✅
```

---

## Safety Rules (Validator)

| Rule | Limit |
|---|---|
| Max speed | 0.5 m/s |
| Min speed | 0.05 m/s |
| Max coordinate | ±20 m from map origin |
| Min waypoints | 2 |
| Max waypoints | 50 |
| Max repeats | 10 |

Any mission that violates these is rejected before the robot moves.

---

## Scaling to Real-World

1. **Swap simulator for real robot** — the executor only uses `nav2_msgs/NavigateToPose`. Any Nav2-compatible robot (real TurtleBot3, Clearpath Husky, etc.) works with zero code changes.
2. **Add GPS waypoints** — replace map-frame x/y with lat/lon + a coordinate converter node.
3. **Multi-robot** — run multiple executor instances with namespaced Nav2 stacks.
4. **Voice input** — pipe Whisper transcription into `run_mission.py` instead of `input()`.
5. **Mission history + audit log** — the validated JSON is already saved to `/tmp/current_mission.json`. Persist these to a database for full auditability.
6. **Fallback on LLM failure** — validator already rejects bad JSON; add retry logic with a simpler fallback prompt.

---

## File Structure

```
omokai-robotics/
├── llm_planner.py        # Prompt → Groq LLM → Mission JSON
├── mission_validator.py  # JSON schema + safety validation
├── mission_executor.py   # ROS 2 Nav2 goal sender (deterministic)
├── run_mission.py        # Pipeline orchestrator
├── omokai.sh             # Single launch script
├── Dockerfile            # Portable container build
├── README.md             # This file
└── SOURCES.md            # Cited sources and licenses
```
