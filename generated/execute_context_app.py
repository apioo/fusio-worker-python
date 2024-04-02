from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
@dataclass_json
@dataclass
class ExecuteContextApp:
    anonymous: bool = field(default=None, metadata=config(field_name="anonymous"))
    id: int = field(default=None, metadata=config(field_name="id"))
    name: str = field(default=None, metadata=config(field_name="name"))
