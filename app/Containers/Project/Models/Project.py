from sqlalchemy import Column, String, Text, Enum, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.Ship.Parents.Models.Model import BaseModel
import enum
import uuid

class ProjectStatus(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class Project(BaseModel):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE)
    
    # Relationships will be defined after all models are imported