from app.Ship.Parents.Actions.Action import Action
from app.Containers.Flow.Tasks.DeleteFlowTask import DeleteFlowTask

class DeleteFlowAction(Action):
    def __init__(self, delete_flow_task: DeleteFlowTask):
        self.delete_flow_task = delete_flow_task
    
    async def run(self, flow_id: int) -> bool:
        """Delete a flow by ID"""
        return await self.delete_flow_task.run(flow_id)