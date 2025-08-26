from sqlalchemy import Column, String, Text, JSON, Enum, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.Ship.Parents.Models.Model import BaseModel
import enum

class FlowStatus(enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    TESTING = "TESTING"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"

class Flow(BaseModel):
    __tablename__ = "flows"
    
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    definition = Column(JSON, nullable=False)  # Flow graph structure
    status = Column(Enum(FlowStatus), default=FlowStatus.DRAFT)
    version = Column(Integer, default=1)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Relationships
    project = relationship("Project", back_populates="flows")
    created_by_user = relationship("User")
    executions = relationship("Execution", back_populates="flow")
    versions = relationship("FlowVersion", back_populates="flow")