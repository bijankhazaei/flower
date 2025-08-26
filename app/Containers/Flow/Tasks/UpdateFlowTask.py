from typing import Optional
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Flow.Data.Repositories.flow_repository import FlowRepository
from app.Containers.Flow.Models.flow import Flow

class UpdateFlowTask(Task):
    def __init__(self, flow_repository: FlowRepository):
        self.flow_repository = flow_repository
    
    async def run(self, flow_id: int, flow_data: dict) -> Optional[Flow]:
        """Update an existing flow"""
        flow = await self.flow_repository.find_by_id(flow_id)
        if not flow:
            return None
        
        # Update flow attributes
        for key, value in flow_data.items():
            if hasattr(flow, key):
                setattr(flow, key, value)
        
        return await self.flow_repository.update(flow)