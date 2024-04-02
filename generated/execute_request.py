from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Any
from typing import Dict
from execute_request_context import ExecuteRequestContext
@dataclass_json
@dataclass
class ExecuteRequest:
    arguments: Dict[str, str] = field(default=None, metadata=config(field_name="arguments"))
    payload: Any = field(default=None, metadata=config(field_name="payload"))
    context: ExecuteRequestContext = field(default=None, metadata=config(field_name="context"))
