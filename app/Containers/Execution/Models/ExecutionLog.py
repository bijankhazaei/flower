from sqlalchemy import Column, String, Text, JSON, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.Ship.Parents.Models.Model import BaseModel


class LogLevel(enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class ExecutionLog(BaseModel):
    __tablename__ = "execution_logs"

    execution_id = Column(UUID(as_uuid=True), ForeignKey('executions.id'), nullable=False)
    node_id = Column(String(255))
    level = Column(Enum(LogLevel), default=LogLevel.INFO, nullable=False)
    message = Column(Text, nullable=False)
    metadata = Column(JSON, default={})
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    execution = relationship("Execution", back_populates="logs")

    def __repr__(self):
        return f"<ExecutionLog(execution_id={self.execution_id}, level='{self.level.value}')>"