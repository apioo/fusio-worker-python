from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class ExecuteRequestContext(BaseModel):
    type: Optional[str] = Field(default=None, alias="type")
    uri_fragments: Optional[Dict[str, str]] = Field(default=None, alias="uriFragments")
    method: Optional[str] = Field(default=None, alias="method")
    path: Optional[str] = Field(default=None, alias="path")
    query_parameters: Optional[Dict[str, str]] = Field(default=None, alias="queryParameters")
    headers: Optional[Dict[str, str]] = Field(default=None, alias="headers")
    pass
