from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
@dataclass_json
@dataclass
class Message:
    success: bool = field(default=None, metadata=config(field_name="success"))
    message: str = field(default=None, metadata=config(field_name="message"))
    trace: str = field(default=None, metadata=config(field_name="trace"))
