from app.Ship.Parents.action import Action
from app.Containers.Flow.Tasks.create_flow_task import CreateFlowTask
from app.Containers.Flow.UI.API.Requests.flow_request import CreateFlowRequest
from app.Containers.Flow.Models.flow import Flow

class CreateFlowAction(Action):
    def __init__(self, create_flow_task: CreateFlowTask):
        self.create_flow_task = create_flow_task
    
    async def run(self, request: CreateFlowRequest) -> Flow:
        return await self.create_flow_task.run(request.dict())