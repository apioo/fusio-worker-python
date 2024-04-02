from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
@dataclass_json
@dataclass
class ExecuteConnection:
    type: str = field(default=None, metadata=config(field_name="type"))
    config: str = field(default=None, metadata=config(field_name="config"))
