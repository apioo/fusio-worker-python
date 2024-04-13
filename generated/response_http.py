from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class ResponseHTTP(BaseModel):
    status_code: Optional[int] = Field(default=None, alias="statusCode")
    headers: Optional[Dict[str, str]] = Field(default=None, alias="headers")
    body: Optional[Any] = Field(default=None, alias="body")
    pass
