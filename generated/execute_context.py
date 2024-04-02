from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from execute_context_app import ExecuteContextApp
from execute_context_user import ExecuteContextUser
@dataclass_json
@dataclass
class ExecuteContext:
    operation_id: int = field(default=None, metadata=config(field_name="operationId"))
    base_url: str = field(default=None, metadata=config(field_name="baseUrl"))
    tenant_id: str = field(default=None, metadata=config(field_name="tenantId"))
    action: str = field(default=None, metadata=config(field_name="action"))
    app: ExecuteContextApp = field(default=None, metadata=config(field_name="app"))
    user: ExecuteContextUser = field(default=None, metadata=config(field_name="user"))
