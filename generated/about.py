from dataclasses import dataclass
from dataclasses_json import dataclass_json
@dataclass_json
@dataclass
class About:
    api_version: str
    language: str
