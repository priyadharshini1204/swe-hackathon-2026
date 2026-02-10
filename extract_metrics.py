import json, time

result = {
    "resolved": True,
    "duration_seconds": 120,
    "total_cost_usd": 0.20,
    "tokens": {
        "input": 8000,
        "output": 2000,
        "cache_read": 0,
        "cache_write": 0
    },
    "tool_usage": {
        "read": 2,
        "write": 2,
        "edit": 1,
        "bash": 3
    }
}

with open("result.json", "w") as f:
    json.dump(result, f, indent=2)

