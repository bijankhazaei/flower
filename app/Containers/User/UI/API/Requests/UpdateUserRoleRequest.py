from pydantic import BaseModel
from app.Containers.User.Models.User import UserRole


class UpdateUserRoleRequest(BaseModel):
    role: UserRole