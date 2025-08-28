from app.Ship.Parents.Actions.Action import Action
from app.Containers.Project.Tasks.GetUserProjectsTask import GetUserProjectsTask
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.Models.Project import Project
from sqlalchemy.orm import Session
from typing import List
import uuid

class GetUserProjectsAction(Action):
    def run(self, user_id: uuid.UUID, db: Session) -> List[Project]:
        project_repository = ProjectRepository(db)
        get_projects_task = GetUserProjectsTask(project_repository)
        return get_projects_task.run(user_id)