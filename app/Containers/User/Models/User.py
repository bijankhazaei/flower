from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from app.Ship.Parents.Models.Model import BaseModel
import enum

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    
    # Relationships
    projects = relationship("UserProject", back_populates="user")
    owned_projects = relationship("Project", back_populates="owner")
    executions = relationship("Execution", back_populates="user")