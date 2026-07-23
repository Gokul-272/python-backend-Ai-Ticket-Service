from datetime import datetime
from typing import Literal, Optional
from pydantic import (BaseModel, ConfigDict, Field, computed_field, field_validator)

class CreateTicketRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    priority: Literal["low", "medium", "high"]
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters after stripping whitespace")
        return value

class UpdateTicketRequest(BaseModel):
    title: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["open", "in_progress", "resolved"]] = None
    assignee: Optional[str] = None
    email: Optional[str] = Field(default=None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if value == "":
            raise ValueError("Title cannot be blank")
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters after stripping whitespace")
        return value

class TicketResponse(BaseModel):
    id: int
    title: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved"]
    created_at: datetime
    assignee: Optional[str] = None
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True) 

    @computed_field
    @property 
    def is_resolved(self) -> bool: 
        return self.status == "resolved"

class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5_000)
 
 
class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str