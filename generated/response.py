from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from .response_http import ResponseHTTP
from .response_event import ResponseEvent
from .response_log import ResponseLog
class Response(BaseModel):
    response: Optional[ResponseHTTP] = Field(default=None, alias="response")
    events: Optional[List[ResponseEvent]] = Field(default=None, alias="events")
    logs: Optional[List[ResponseLog]] = Field(default=None, alias="logs")
    pass
