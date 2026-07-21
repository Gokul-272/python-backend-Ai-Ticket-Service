from datetime import datetime
from typing import Literal, Optional
from pydantic import (BaseModel, ConfigDict,Field, computed_field,field_validator)

class CreateTicketRequest(BaseModel):
    title: str = Field(...,min_length=3,max_length=100)
    priority: Literal["low","medium","high"]

class UpdateTicketRequest(BaseModel):
    title: Optional[str] = None
    priority: Optional[Literal["low","medium","high"]] = None
    status: Optional[Literal["open","in_progress","resolved"]] = None
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value
        value = value.strip()
        if value == "":
            raise ValueError("Title cannot be blank")
        return value

class TicketResponse(BaseModel):
    id: int
    title: str
    priority: Literal["low","medium","high"]
    status: Literal["open","in_progress","resolved"]
    created_at: datetime
    assignee: Optional[str] = None
    model_config = ConfigDict(from_attributes=True) 
    @computed_field
    @property 
    def is_resolved(self) -> bool: 
        return self.status == "resolved"
