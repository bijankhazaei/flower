from typing import List, Optional
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Flow.Data.Repositories.FlowTemplateRepository import FlowTemplateRepository
from app.Containers.Flow.Models.FlowTemplate import FlowTemplate

class GetTemplatesTask(Task):
    def __init__(self, template_repository: FlowTemplateRepository):
        self.template_repository = template_repository
    
    async def run(self, category: Optional[str] = None, user_id: Optional[int] = None, 
                  public_only: bool = False) -> List[FlowTemplate]:
        """Get templates with optional filtering"""
        if public_only:
            return await self.template_repository.find_public_templates()
        elif user_id:
            return await self.template_repository.find_by_user(user_id)
        elif category:
            return await self.template_repository.find_by_category(category)
        else:
            return await self.template_repository.find_all()