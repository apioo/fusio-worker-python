from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class ExecuteContextUser(BaseModel):
    anonymous: Optional[bool] = Field(default=None, alias="anonymous")
    id: Optional[int] = Field(default=None, alias="id")
    plan_id: Optional[str] = Field(default=None, alias="planId")
    name: Optional[str] = Field(default=None, alias="name")
    email: Optional[str] = Field(default=None, alias="email")
    points: Optional[int] = Field(default=None, alias="points")
    pass
