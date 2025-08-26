from sqlalchemy import Column, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.Ship.Parents.Models.Model import Model


class UserProjectRole(enum.Enum):
    OWNER = "OWNER"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"


class UserProject(Model):
    __tablename__ = "user_projects"

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), primary_key=True)
    role = Column(Enum(UserProjectRole), default=UserProjectRole.VIEWER, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="users")

    def __repr__(self):
        return f"<UserProject(user_id={self.user_id}, project_id={self.project_id}, role='{self.role.value}')>"