from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Any
from typing import Dict
@dataclass_json
@dataclass
class ResponseHTTP:
    status_code: int = field(default=None, metadata=config(field_name="statusCode"))
    headers: Dict[str, str] = field(default=None, metadata=config(field_name="headers"))
    body: Any = field(default=None, metadata=config(field_name="body"))
