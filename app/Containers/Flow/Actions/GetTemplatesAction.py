from typing import List
from app.Ship.Parents.Actions.Action import Action
from app.Containers.Flow.Tasks.GetTemplatesTask import GetTemplatesTask
from app.Containers.Flow.Models.FlowTemplate import FlowTemplate

class GetTemplatesAction(Action):
    def __init__(self, get_templates_task: GetTemplatesTask):
        self.get_templates_task = get_templates_task
    
    async def run(self, filters: dict = None) -> List[FlowTemplate]:
        """Get templates with optional filtering"""
        filters = filters or {}
        return await self.get_templates_task.run(
            category=filters.get("category"),
            user_id=filters.get("user_id"),
            public_only=filters.get("public_only", False)
        )