from typing import Dict, Any
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.Models.Project import Project


class CreateProjectTask(Task):
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def run(self, name: str, description: str, owner_id: str, settings: Dict[str, Any] = None) -> Project:
        """Create a new project"""
        # Validate input
        if not name or not name.strip():
            raise ValueError("Project name is required")
        
        if not owner_id:
            raise ValueError("Owner ID is required")
        
        # Create project
        project = await self.project_repository.create_project(
            name=name.strip(),
            description=description or "",
            owner_id=owner_id,
            settings=settings or {}
        )
        
        return project