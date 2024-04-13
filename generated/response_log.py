from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class ResponseLog(BaseModel):
    level: Optional[str] = Field(default=None, alias="level")
    message: Optional[str] = Field(default=None, alias="message")
    pass
