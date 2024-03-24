from dataclasses import dataclass
from dataclasses_json import dataclass_json
@dataclass_json
@dataclass
class ExecuteContextUser:
    anonymous: bool
    id: int
    plan_id: str
    name: str
    email: str
    points: int
