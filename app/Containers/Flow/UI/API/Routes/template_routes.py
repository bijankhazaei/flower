from fastapi import APIRouter
from app.Containers.Flow.UI.API.Controllers.TemplateController import TemplateController

controller = TemplateController()
router = controller.router