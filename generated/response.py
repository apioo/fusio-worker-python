from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import List
from response_http import ResponseHTTP
from response_event import ResponseEvent
from response_log import ResponseLog
@dataclass_json
@dataclass
class Response:
    response: ResponseHTTP = field(default=None, metadata=config(field_name="response"))
    events: List[ResponseEvent] = field(default=None, metadata=config(field_name="events"))
    logs: List[ResponseLog] = field(default=None, metadata=config(field_name="logs"))
