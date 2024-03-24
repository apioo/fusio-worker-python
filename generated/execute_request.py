from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any
from typing import Dict
from execute_request_context import ExecuteRequestContext
@dataclass_json
@dataclass
class ExecuteRequest:
    arguments: Dict[str, str]
    payload: Any
    context: ExecuteRequestContext
