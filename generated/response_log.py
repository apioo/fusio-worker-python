from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
@dataclass_json
@dataclass
class ResponseLog:
    level: str = field(default=None, metadata=config(field_name="level"))
    message: str = field(default=None, metadata=config(field_name="message"))
