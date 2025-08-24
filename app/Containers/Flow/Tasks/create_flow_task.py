from app.Ship.Parents.task import Task
from app.Containers.Flow.Models.flow import Flow
from app.Containers.Flow.Data.Repositories.flow_repository import FlowRepository
from typing import Dict, Any

class CreateFlowTask(Task):
    def __init__(self, flow_repository: FlowRepository):
        self.flow_repository = flow_repository
    
    async def run(self, data: Dict[str, Any]) -> Flow:
        return await self.flow_repository.create(data)