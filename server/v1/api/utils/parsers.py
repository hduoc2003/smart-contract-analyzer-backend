from enum import Enum
import json
from typing import Any

def obj_to_jsonstr(obj: object) -> str:
    return json.dumps(
        obj,
        default=lambda o:
            o.value if isinstance(o, Enum) else o.__dict__,
        indent=2)

def obj_to_json(o: object) -> dict[str, Any]:
    return json.loads(obj_to_jsonstr(o))
