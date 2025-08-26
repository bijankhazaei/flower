from typing import Optional
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Flow.Data.Repositories.flow_repository import FlowRepository
from app.Containers.Flow.Models.flow import Flow

class GetFlowTask(Task):
    def __init__(self, flow_repository: FlowRepository):
        self.flow_repository = flow_repository
    
    async def run(self, flow_id: int) -> Optional[Flow]:
        """Get a flow by ID"""
        return await self.flow_repository.find_by_id(flow_id)