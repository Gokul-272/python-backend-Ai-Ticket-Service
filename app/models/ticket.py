from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import validates

from app.core.database import Base


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    priority = Column(SQLEnum(PriorityEnum), nullable=False)
    status = Column(SQLEnum(StatusEnum),nullable=False,default=StatusEnum.OPEN,)
    assignee = Column(String(255), nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)
    email = Column(String(255), nullable=True)
    @validates("title")
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        return value 