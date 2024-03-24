from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Dict
from execute_connection import ExecuteConnection
from execute_request import ExecuteRequest
from execute_context import ExecuteContext
@dataclass_json
@dataclass
class Execute:
    connections: Dict[str, ExecuteConnection]
    request: ExecuteRequest
    context: ExecuteContext
