from typing import List, Optional
from app.Ship.Parents.Actions.Action import Action
from app.Containers.Project.Tasks.GetProjectsTask import GetProjectsTask
from app.Containers.Project.Models.Project import Project, ProjectStatus


class GetProjectsAction(Action):
    def __init__(self, get_projects_task: GetProjectsTask):
        self.get_projects_task = get_projects_task

    async def run(self, user_id: str, status: Optional[ProjectStatus] = None, owned_only: bool = False) -> List[Project]:
        """Get projects accessible to a user"""
        try:
            projects = await self.get_projects_task.run(
                user_id=user_id,
                status=status,
                owned_only=owned_only
            )
            
            return projects
            
        except ValueError as e:
            raise ValueError(f"Failed to retrieve projects: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error retrieving projects: {str(e)}")