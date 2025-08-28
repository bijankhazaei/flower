from app.Ship.Parents.Actions.Action import Action
from app.Containers.Project.Tasks.CreateProjectTask import CreateProjectTask
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.Models.Project import Project
from sqlalchemy.orm import Session

class CreateProjectAction(Action):
    def run(self, project_data: dict, db: Session) -> Project:
        project_repository = ProjectRepository(db)
        create_project_task = CreateProjectTask(project_repository)
        return create_project_task.run(project_data)