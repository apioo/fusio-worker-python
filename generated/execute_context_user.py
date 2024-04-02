from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
@dataclass_json
@dataclass
class ExecuteContextUser:
    anonymous: bool = field(default=None, metadata=config(field_name="anonymous"))
    id: int = field(default=None, metadata=config(field_name="id"))
    plan_id: str = field(default=None, metadata=config(field_name="planId"))
    name: str = field(default=None, metadata=config(field_name="name"))
    email: str = field(default=None, metadata=config(field_name="email"))
    points: int = field(default=None, metadata=config(field_name="points"))
