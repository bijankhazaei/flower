from typing import List, Optional
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Flow.Data.Repositories.flow_repository import FlowRepository
from app.Containers.Flow.Models.flow import Flow

class GetFlowsTask(Task):
    def __init__(self, flow_repository: FlowRepository):
        self.flow_repository = flow_repository
    
    async def run(self, user_id: Optional[int] = None) -> List[Flow]:
        """Get all flows, optionally filtered by user"""
        if user_id:
            return await self.flow_repository.find_by_user_id(user_id)
        return await self.flow_repository.find_all()