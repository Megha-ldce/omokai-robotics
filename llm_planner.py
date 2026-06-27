import os
import json
import re
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY environment variable not set.")
    print("Get a free key at https://console.groq.com (no credit card needed)")
    print("Then run: export GROQ_API_KEY=your_key_here")
    exit(1)

SYSTEM_PROMPT = """You are a robot mission planner. Convert natural language commands into a structured mission JSON for a ground robot.

Output ONLY valid JSON, nothing else. No explanation, no markdown, no code blocks.

Schema:
{
  "mission_name": "string",
  "repeat": integer (how many times to run the full waypoint list),
  "speed": float (m/s, max 0.5),
  "waypoints": [
    {"x": float, "y": float, "label": "string"}
  ]
}

Rules:
- Speed must be between 0.05 and 0.5 m/s
- At least 2 waypoints required
- x,y are in MAP frame coordinates. Robot starts at map position (-2.0, -0.5). So robot start = (-2.0, -0.5), 2m forward = (-2.0+2, -0.5) = (0.0, -0.5), etc.
- For loops, always return to (-2.0, -0.5) as the final waypoint
- "repeat" defaults to 1 if not specified
- For "patrol loop" or "perimeter" commands, last waypoint should return near (0,0)
- Waypoints must form a logical path (square, loop, line, etc.)

Examples of valid missions:
- "Drive a 2m square" → 4 corner waypoints forming a square
- "Patrol a loop twice" → loop waypoints with repeat=2
- "Go forward 3m and come back" → two waypoints
"""

def prompt_to_mission(user_prompt: str) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,  # low temp = more deterministic JSON
        max_tokens=500
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown code blocks if model adds them anyway
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)

if __name__ == "__main__":
    test_prompts = [
        "Drive a 2 metre square loop",
        "Patrol the perimeter twice at slow speed",
        "Go forward 3 metres and return to start",
    ]
    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        mission = prompt_to_mission(prompt)
        print(json.dumps(mission, indent=2))
