from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Dict
@dataclass_json
@dataclass
class ExecuteRequestContext:
    type: str = field(default=None, metadata=config(field_name="type"))
    uri_fragments: Dict[str, str] = field(default=None, metadata=config(field_name="uriFragments"))
    method: str = field(default=None, metadata=config(field_name="method"))
    path: str = field(default=None, metadata=config(field_name="path"))
    query_parameters: Dict[str, str] = field(default=None, metadata=config(field_name="queryParameters"))
    headers: Dict[str, str] = field(default=None, metadata=config(field_name="headers"))
