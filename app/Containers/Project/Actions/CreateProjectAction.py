from app.Ship.Parents.Actions.Action import Action
from app.Containers.Project.Tasks.CreateProjectTask import CreateProjectTask
from app.Containers.Project.UI.API.Requests.CreateProjectRequest import CreateProjectRequest


class CreateProjectAction(Action):
    def __init__(self, create_project_task: CreateProjectTask):
        self.create_project_task = create_project_task

    def run(self, request: CreateProjectRequest, user_id: str):
        return self.create_project_task.run(
            name=request.name,
            description=request.description,
            owner_id=user_id,
            settings=request.settings or {}
        )