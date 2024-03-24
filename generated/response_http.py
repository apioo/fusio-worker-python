from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any
from typing import Dict
@dataclass_json
@dataclass
class ResponseHTTP:
    status_code: int
    headers: Dict[str, str]
    body: Any
