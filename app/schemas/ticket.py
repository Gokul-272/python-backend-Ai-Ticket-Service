from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    priority: TicketPriority

class TicketUpdate(BaseModel):
    status: TicketStatus