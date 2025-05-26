from typing import Any, Dict
import hashlib
import json

def generate_hash(data: Dict[str, Any]) -> str:
    serialized = json.dumps(data, sort_keys=True)
    return hashlib.md5(serialized.encode()).hexdigest()

def format_distance(meters: float) -> str:
    if meters < 1000:
        return f"{int(meters)}m"
    else:
        return f"{meters/1000:.1f}km"
