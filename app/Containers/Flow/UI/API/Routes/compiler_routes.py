from fastapi import APIRouter, Depends
from app.Containers.Flow.UI.API.Controllers.CompilerController import CompilerController
from app.Containers.Flow.UI.API.Requests.CompileFlowRequest import CompileFlowRequest
from app.Containers.Flow.UI.API.Requests.ExecuteFlowRequest import ExecuteFlowRequest

router = APIRouter(prefix="/compiler", tags=["Flow Compiler"])

def get_compiler_controller() -> CompilerController:
    return CompilerController()

@router.post("/compile")
async def compile_flow(
    request: CompileFlowRequest,
    controller: CompilerController = Depends(get_compiler_controller)
):
    """Compile a visual flow to executable code"""
    return await controller.compile_flow(request)

@router.post("/validate")
async def validate_flow(
    request: CompileFlowRequest,
    controller: CompilerController = Depends(get_compiler_controller)
):
    """Validate a flow definition"""
    return await controller.validate_flow(request)

@router.post("/execute")
async def execute_flow(
    request: ExecuteFlowRequest,
    controller: CompilerController = Depends(get_compiler_controller)
):
    """Execute a flow with given inputs"""
    return await controller.execute_flow(request)