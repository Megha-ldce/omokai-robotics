import json

MAX_SPEED = 0.5
MIN_SPEED = 0.05
MAX_WAYPOINTS = 50
MAX_COORD = 20.0  # metres, safety boundary

def validate_mission(mission: dict) -> tuple[bool, list[str]]:
    errors = []

    # Check required top-level keys
    for key in ["mission_name", "repeat", "speed", "waypoints"]:
        if key not in mission:
            errors.append(f"Missing required field: '{key}'")

    if errors:
        return False, errors

    # Validate speed
    speed = mission["speed"]
    if not isinstance(speed, (int, float)):
        errors.append(f"Speed must be a number, got {type(speed)}")
    elif speed < MIN_SPEED or speed > MAX_SPEED:
        errors.append(f"Speed {speed} out of range [{MIN_SPEED}, {MAX_SPEED}] m/s")

    # Validate repeat
    repeat = mission["repeat"]
    if not isinstance(repeat, int) or repeat < 1 or repeat > 10:
        errors.append(f"repeat must be integer between 1 and 10, got {repeat}")

    # Validate waypoints
    waypoints = mission["waypoints"]
    if not isinstance(waypoints, list):
        errors.append("waypoints must be a list")
    elif len(waypoints) < 2:
        errors.append(f"Need at least 2 waypoints, got {len(waypoints)}")
    elif len(waypoints) > MAX_WAYPOINTS:
        errors.append(f"Too many waypoints: {len(waypoints)} > {MAX_WAYPOINTS}")
    else:
        for i, wp in enumerate(waypoints):
            if "x" not in wp or "y" not in wp:
                errors.append(f"Waypoint {i} missing x or y")
                continue
            if not isinstance(wp["x"], (int, float)) or not isinstance(wp["y"], (int, float)):
                errors.append(f"Waypoint {i} x,y must be numbers")
                continue
            if abs(wp["x"]) > MAX_COORD or abs(wp["y"]) > MAX_COORD:
                errors.append(f"Waypoint {i} out of safety boundary (max {MAX_COORD}m): ({wp['x']}, {wp['y']})")

    if errors:
        return False, errors
    return True, []


def validate_and_report(mission: dict) -> dict:
    ok, errors = validate_mission(mission)
    if ok:
        print(f"[VALIDATOR] ✅ Mission '{mission['mission_name']}' passed all checks.")
        return mission
    else:
        print(f"[VALIDATOR] ❌ Mission REJECTED:")
        for e in errors:
            print(f"  - {e}")
        raise ValueError(f"Mission failed validation: {errors}")


if __name__ == "__main__":
    # Test 1: valid mission
    good = {
        "mission_name": "Test Square",
        "repeat": 1,
        "speed": 0.2,
        "waypoints": [
            {"x": 0.0, "y": 0.0, "label": "Start"},
            {"x": 2.0, "y": 0.0, "label": "A"},
            {"x": 2.0, "y": 2.0, "label": "B"},
            {"x": 0.0, "y": 0.0, "label": "End"},
        ]
    }

    # Test 2: bad mission (speed too high, waypoint out of bounds)
    bad = {
        "mission_name": "Dangerous Run",
        "repeat": 1,
        "speed": 5.0,
        "waypoints": [
            {"x": 0.0, "y": 0.0, "label": "Start"},
            {"x": 999.0, "y": 0.0, "label": "Way too far"},
        ]
    }

    print("--- Test 1: Good mission ---")
    validate_and_report(good)

    print("\n--- Test 2: Bad mission ---")
    try:
        validate_and_report(bad)
    except ValueError:
        pass
