from app.Ship.Parents.Actions.Action import Action
from app.Containers.Flow.Tasks.CreateTemplateTask import CreateTemplateTask
from app.Containers.Flow.Models.FlowTemplate import FlowTemplate

class CreateTemplateAction(Action):
    def __init__(self, create_template_task: CreateTemplateTask):
        self.create_template_task = create_template_task
    
    async def run(self, template_data: dict) -> FlowTemplate:
        """Create a new flow template"""
        return await self.create_template_task.run(
            name=template_data["name"],
            description=template_data.get("description", ""),
            flow_definition=template_data["flow_definition"],
            category=template_data.get("category"),
            is_public=template_data.get("is_public", False),
            created_by=template_data.get("created_by")
        )