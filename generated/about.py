from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
@dataclass_json
@dataclass
class About:
    api_version: str = field(default=None, metadata=config(field_name="apiVersion"))
    language: str = field(default=None, metadata=config(field_name="language"))
