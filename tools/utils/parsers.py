from enum import Enum
import json

def obj_to_jsonstr(obj: object) -> str:
    return json.dumps(
        obj,
        default=lambda o:
            o.value if isinstance(o, Enum) else o.__dict__,
        indent=2)

def obj_to_json(obj: object) -> dict:
    return json.loads(json.dumps(
        obj,
        default=lambda o:
            o.value if isinstance(o, Enum) else o.__dict__,
        indent=2)
    )
