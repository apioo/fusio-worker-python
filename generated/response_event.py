from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class ResponseEvent(BaseModel):
    event_name: Optional[str] = Field(default=None, alias="eventName")
    data: Optional[Any] = Field(default=None, alias="data")
    pass
