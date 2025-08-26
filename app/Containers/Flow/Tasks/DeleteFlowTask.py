from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Flow.Data.Repositories.flow_repository import FlowRepository

class DeleteFlowTask(Task):
    def __init__(self, flow_repository: FlowRepository):
        self.flow_repository = flow_repository
    
    async def run(self, flow_id: int) -> bool:
        """Delete a flow by ID"""
        flow = await self.flow_repository.find_by_id(flow_id)
        if not flow:
            return False
        
        await self.flow_repository.delete(flow)
        return True