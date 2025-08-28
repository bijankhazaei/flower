from pydantic import BaseModel
from app.Containers.Project.Models.Project import ProjectStatus
from typing import Optional
import uuid

class CreateProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: uuid.UUID
    status: Optional[ProjectStatus] = ProjectStatus.ACTIVE