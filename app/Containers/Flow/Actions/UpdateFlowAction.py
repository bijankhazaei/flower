from typing import Optional
from app.Ship.Parents.Actions.Action import Action
from app.Containers.Flow.Tasks.UpdateFlowTask import UpdateFlowTask
from app.Containers.Flow.Models.flow import Flow

class UpdateFlowAction(Action):
    def __init__(self, update_flow_task: UpdateFlowTask):
        self.update_flow_task = update_flow_task
    
    async def run(self, flow_id: int, flow_data: dict) -> Optional[Flow]:
        """Update an existing flow"""
        return await self.update_flow_task.run(flow_id, flow_data)