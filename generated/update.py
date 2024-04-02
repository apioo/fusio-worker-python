from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
@dataclass_json
@dataclass
class Update:
    code: str = field(default=None, metadata=config(field_name="code"))
