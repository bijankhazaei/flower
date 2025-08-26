import json
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Flow.Data.Repositories.FlowTemplateRepository import FlowTemplateRepository
from app.Containers.Flow.Models.FlowTemplate import FlowTemplate

class CreateTemplateTask(Task):
    def __init__(self, template_repository: FlowTemplateRepository):
        self.template_repository = template_repository
    
    async def run(self, name: str, description: str, flow_definition: dict, 
                  category: str = None, is_public: bool = False, created_by: int = None) -> FlowTemplate:
        """Create a new flow template"""
        template_data = {
            "name": name,
            "description": description,
            "category": category,
            "template_data": json.dumps(flow_definition),
            "is_public": is_public,
            "created_by": created_by
        }
        
        return await self.template_repository.create(template_data)