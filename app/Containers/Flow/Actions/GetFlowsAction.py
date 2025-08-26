from typing import List, Optional
from app.Ship.Parents.Actions.Action import Action
from app.Containers.Flow.Tasks.GetFlowsTask import GetFlowsTask
from app.Containers.Flow.Models.flow import Flow

class GetFlowsAction(Action):
    def __init__(self, get_flows_task: GetFlowsTask):
        self.get_flows_task = get_flows_task
    
    async def run(self, user_id: Optional[int] = None) -> List[Flow]:
        """Get all flows, optionally filtered by user"""
        return await self.get_flows_task.run(user_id)