from typing import Dict, Any
from app.Ship.Parents.Actions.Action import Action
from app.Containers.Project.Tasks.CreateProjectTask import CreateProjectTask
from app.Containers.Project.Models.Project import Project


class CreateProjectAction(Action):
    def __init__(self, create_project_task: CreateProjectTask):
        self.create_project_task = create_project_task

    async def run(self, name: str, description: str, owner_id: str, settings: Dict[str, Any] = None) -> Project:
        """Create a new project"""
        try:
            project = await self.create_project_task.run(
                name=name,
                description=description,
                owner_id=owner_id,
                settings=settings
            )
            
            return project
            
        except ValueError as e:
            raise ValueError(f"Project creation failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error during project creation: {str(e)}")