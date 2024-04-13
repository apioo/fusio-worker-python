from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from .execute_connection import ExecuteConnection
from .execute_request import ExecuteRequest
from .execute_context import ExecuteContext
class Execute(BaseModel):
    connections: Optional[Dict[str, ExecuteConnection]] = Field(default=None, alias="connections")
    request: Optional[ExecuteRequest] = Field(default=None, alias="request")
    context: Optional[ExecuteContext] = Field(default=None, alias="context")
    pass
