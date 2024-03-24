from dataclasses import dataclass
from dataclasses_json import dataclass_json
from execute_context_app import ExecuteContextApp
from execute_context_user import ExecuteContextUser
@dataclass_json
@dataclass
class ExecuteContext:
    operation_id: int
    base_url: str
    tenant_id: str
    action: str
    app: ExecuteContextApp
    user: ExecuteContextUser
