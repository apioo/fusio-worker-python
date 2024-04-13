from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from .execute_context_app import ExecuteContextApp
from .execute_context_user import ExecuteContextUser
class ExecuteContext(BaseModel):
    operation_id: Optional[int] = Field(default=None, alias="operationId")
    base_url: Optional[str] = Field(default=None, alias="baseUrl")
    tenant_id: Optional[str] = Field(default=None, alias="tenantId")
    action: Optional[str] = Field(default=None, alias="action")
    app: Optional[ExecuteContextApp] = Field(default=None, alias="app")
    user: Optional[ExecuteContextUser] = Field(default=None, alias="user")
    pass
