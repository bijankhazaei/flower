from typing import Optional
from app.Ship.Parents.Actions.Action import Action
from app.Containers.Flow.Tasks.GetFlowTask import GetFlowTask
from app.Containers.Flow.Models.flow import Flow

class GetFlowAction(Action):
    def __init__(self, get_flow_task: GetFlowTask):
        self.get_flow_task = get_flow_task
    
    async def run(self, flow_id: int) -> Optional[Flow]:
        """Get a flow by ID"""
        return await self.get_flow_task.run(flow_id)