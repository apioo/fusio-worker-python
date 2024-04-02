from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Dict
from execute_connection import ExecuteConnection
from execute_request import ExecuteRequest
from execute_context import ExecuteContext
@dataclass_json
@dataclass
class Execute:
    connections: Dict[str, ExecuteConnection] = field(default=None, metadata=config(field_name="connections"))
    request: ExecuteRequest = field(default=None, metadata=config(field_name="request"))
    context: ExecuteContext = field(default=None, metadata=config(field_name="context"))
