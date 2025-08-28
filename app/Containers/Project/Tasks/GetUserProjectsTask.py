from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Project.Models.Project import Project
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from typing import List
import uuid

class GetUserProjectsTask(Task):
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
    
    def run(self, user_id: uuid.UUID) -> List[Project]:
        return self.project_repository.find_by_user(user_id)