from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.Containers.Flow.Actions.CreateTemplateAction import CreateTemplateAction
from app.Containers.Flow.Actions.GetTemplatesAction import GetTemplatesAction
from app.Containers.Flow.UI.API.Requests.TemplateRequest import CreateTemplateRequest

class TemplateController:
    def __init__(self):
        self.router = APIRouter(prefix="/templates", tags=["Template Management"])
        self.setup_routes()
    
    def setup_routes(self):
        self.router.add_api_route("/", self.create_template, methods=["POST"])
        self.router.add_api_route("/", self.get_templates, methods=["GET"])
        self.router.add_api_route("/{template_id}", self.get_template, methods=["GET"])
    
    async def create_template(self, request: CreateTemplateRequest):
        # TODO: Get user_id from authentication
        template_data = request.dict()
        template_data["created_by"] = 1  # Placeholder
        
        action = CreateTemplateAction(None)  # TODO: Dependency injection
        template = await action.run(template_data)
        return {"id": template.id, "name": template.name, "message": "Template created successfully"}
    
    async def get_templates(self, 
                           category: Optional[str] = Query(None),
                           user_id: Optional[int] = Query(None),
                           public_only: Optional[bool] = Query(False)):
        filters = {"category": category, "user_id": user_id, "public_only": public_only}
        action = GetTemplatesAction(None)  # TODO: Dependency injection
        templates = await action.run(filters)
        
        return [{
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "category": t.category,
            "is_public": t.is_public,
            "created_at": t.created_at
        } for t in templates]
    
    async def get_template(self, template_id: int):
        # TODO: Implement get single template
        return {"message": "Template details endpoint"}