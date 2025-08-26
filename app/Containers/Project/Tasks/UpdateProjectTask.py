from typing import Dict, Any, Optional
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.Models.Project import Project, ProjectStatus
from app.Containers.Project.Models.UserProject import UserProjectRole


class UpdateProjectTask(Task):
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    async def run(self, project_id: str, user_id: str, updates: Dict[str, Any]) -> Optional[Project]:
        """Update project details"""
        if not project_id or not user_id:
            raise ValueError("Project ID and User ID are required")
        
        # Check if user has permission to update project
        has_access = await self.project_repository.user_has_access(
            user_id, project_id, UserProjectRole.EDITOR
        )
        
        if not has_access:
            raise PermissionError("User does not have permission to update this project")
        
        # Validate updates
        allowed_fields = {'name', 'description', 'settings', 'status'}
        filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields}
        
        if 'name' in filtered_updates and not filtered_updates['name'].strip():
            raise ValueError("Project name cannot be empty")
        
        # Update project
        project = await self.project_repository.update_project(project_id, filtered_updates)
        
        if not project:
            raise ValueError("Project not found")
        
        return project