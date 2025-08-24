from sqlalchemy import Column, String, Enum
from app.Ship.Parents.model import BaseModel
import enum

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)