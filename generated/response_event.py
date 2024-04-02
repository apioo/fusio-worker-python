from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Any
@dataclass_json
@dataclass
class ResponseEvent:
    event_name: str = field(default=None, metadata=config(field_name="eventName"))
    data: Any = field(default=None, metadata=config(field_name="data"))
