from typing import List, Optional
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.Models.Project import Project, ProjectStatus


class GetProjectsTask(Task):
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def run(self, user_id: str, status: Optional[ProjectStatus] = None, owned_only: bool = False) -> List[Project]:
        """Get projects accessible to a user"""
        if not user_id:
            raise ValueError("User ID is required")
        
        if owned_only:
            # Get only projects owned by the user
            projects = await self.project_repository.get_owned_projects(user_id, status)
        else:
            # Get all projects user has access to
            projects = await self.project_repository.get_user_projects(user_id, status)
        
        return projects