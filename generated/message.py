from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class Message(BaseModel):
    success: Optional[bool] = Field(default=None, alias="success")
    message: Optional[str] = Field(default=None, alias="message")
    trace: Optional[str] = Field(default=None, alias="trace")
    pass
