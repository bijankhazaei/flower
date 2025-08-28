from sqlalchemy import Column, ForeignKey, Enum, DateTime, UUID
from sqlalchemy.orm import relationship
from app.Ship.Parents.Models.Model import Base
from datetime import datetime
import enum
import uuid

class UserProjectRole(enum.Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"

class UserProject(Base):
    __tablename__ = "user_projects"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), primary_key=True)
    role = Column(Enum(UserProjectRole), default=UserProjectRole.VIEWER)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships will be defined after all models are imported