from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class ExecuteConnection(BaseModel):
    type: Optional[str] = Field(default=None, alias="type")
    config: Optional[str] = Field(default=None, alias="config")
    pass
