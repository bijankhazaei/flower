from fastapi import APIRouter, Depends, Path
from app.Containers.Node.UI.API.Controllers.NodeController import NodeController
from app.Containers.Node.UI.API.Requests.NodeConfigRequest import NodeConfigRequest

router = APIRouter(prefix="/nodes", tags=["Node Management"])

def get_node_controller() -> NodeController:
    return NodeController()

@router.get("/types")
async def list_node_types(
    controller: NodeController = Depends(get_node_controller)
):
    """List all available node types"""
    return await controller.list_node_types()

@router.get("/types/{node_type}")
async def get_node_info(
    node_type: str = Path(..., description="Node type name"),
    controller: NodeController = Depends(get_node_controller)
):
    """Get detailed information about a specific node type"""
    return await controller.get_node_info(node_type)

@router.post("/validate")
async def validate_node_config(
    request: NodeConfigRequest,
    controller: NodeController = Depends(get_node_controller)
):
    """Validate node configuration"""
    return await controller.validate_node_config(request.node_type, request.config)