from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Enum, Text
from sqlalchemy.orm import relationship
from app.Ship.Parents.model import BaseModel
import enum

class ExecutionStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Execution(BaseModel):
    __tablename__ = "executions"
    
    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False)
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING)
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    execution_time = Column(Integer)  # milliseconds
    
    flow = relationship("Flow", back_populates="executions")