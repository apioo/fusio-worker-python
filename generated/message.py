from dataclasses import dataclass
from dataclasses_json import dataclass_json
@dataclass_json
@dataclass
class Message:
    success: bool
    message: str
    trace: str
