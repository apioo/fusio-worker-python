from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class Update(BaseModel):
    code: Optional[str] = Field(default=None, alias="code")
    pass
