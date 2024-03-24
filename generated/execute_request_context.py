from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Dict
@dataclass_json
@dataclass
class ExecuteRequestContext:
    type: str
    uri_fragments: Dict[str, str]
    method: str
    path: str
    query_parameters: Dict[str, str]
    headers: Dict[str, str]
