from typing import Dict, Any, Optional
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.Models.Project import Project


class CreateProjectTask(Task):
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def run(self, name: str, owner_id: str, description: Optional[str] = None, settings: Optional[Dict[str, Any]] = None) -> Project:
        project_data = {
            "name": name,
            "owner_id": owner_id,
            "description": description,
            "settings": settings or {}
        }
        
        return self.project_repository.create(project_data)