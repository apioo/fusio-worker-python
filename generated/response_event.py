from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any
@dataclass_json
@dataclass
class ResponseEvent:
    event_name: str
    data: Any
