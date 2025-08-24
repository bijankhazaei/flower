from fastapi import APIRouter
from app.Containers.Flow.UI.API.Controllers.flow_controller import FlowController

controller = FlowController()
router = controller.router