from pydantic import BaseModel
from app.Containers.User.Models.User import UserStatus


class UpdateUserStatusRequest(BaseModel):
    status: UserStatus