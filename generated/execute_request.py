from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from .execute_request_context import ExecuteRequestContext
class ExecuteRequest(BaseModel):
    arguments: Optional[Dict[str, str]] = Field(default=None, alias="arguments")
    payload: Optional[Any] = Field(default=None, alias="payload")
    context: Optional[ExecuteRequestContext] = Field(default=None, alias="context")
    pass
