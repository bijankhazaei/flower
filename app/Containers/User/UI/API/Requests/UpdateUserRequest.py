from pydantic import BaseModel, EmailStr
from typing import Optional
from app.Containers.User.Models.User import UserRole, UserStatus

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None