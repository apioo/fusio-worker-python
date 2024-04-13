from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
class About(BaseModel):
    api_version: Optional[str] = Field(default=None, alias="apiVersion")
    language: Optional[str] = Field(default=None, alias="language")
    pass
