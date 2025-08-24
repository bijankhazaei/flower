from pydantic import BaseModel, EmailStr
from app.Containers.User.Models.User import UserRole, UserStatus

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE