from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
from response_http import ResponseHTTP
from response_event import ResponseEvent
from response_log import ResponseLog
@dataclass_json
@dataclass
class Response:
    response: ResponseHTTP
    events: List[ResponseEvent]
    logs: List[ResponseLog]
