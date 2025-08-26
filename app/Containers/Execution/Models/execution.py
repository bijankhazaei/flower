from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Enum, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.Ship.Parents.Models.Model import BaseModel
import enum

class ExecutionStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"

class Execution(BaseModel):
    __tablename__ = "executions"
    
    flow_id = Column(UUID(as_uuid=True), ForeignKey("flows.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING)
    inputs = Column(JSON)
    outputs = Column(JSON)
    error_message = Column(Text)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    execution_time_ms = Column(Integer)
    node_results = Column(JSON, default={})
    
    # Relationships
    flow = relationship("Flow", back_populates="executions")
    user = relationship("User", back_populates="executions")
    logs = relationship("ExecutionLog", back_populates="execution")