from fastapi import APIRouter, Depends, Path, Query
from typing import Optional
from app.Containers.Execution.UI.API.Controllers.ExecutionController import ExecutionController

router = APIRouter(prefix="/executions", tags=["Execution Monitoring"])

def get_execution_controller() -> ExecutionController:
    return ExecutionController()

@router.get("/{execution_id}")
async def get_execution(
    execution_id: str = Path(..., description="Execution ID"),
    controller: ExecutionController = Depends(get_execution_controller)
):
    """Get execution details by ID"""
    return await controller.get_execution(execution_id)

@router.get("/")
async def list_executions(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of executions to return"),
    status: Optional[str] = Query(None, description="Filter by execution status"),
    controller: ExecutionController = Depends(get_execution_controller)
):
    """List recent executions"""
    return await controller.list_executions(limit, status)

@router.post("/{execution_id}/cancel")
async def cancel_execution(
    execution_id: str = Path(..., description="Execution ID"),
    controller: ExecutionController = Depends(get_execution_controller)
):
    """Cancel a running execution"""
    return await controller.cancel_execution(execution_id)

@router.post("/cleanup")
async def cleanup_executions(
    max_age_hours: int = Query(24, ge=1, description="Maximum age in hours for executions to keep"),
    controller: ExecutionController = Depends(get_execution_controller)
):
    """Clean up old completed executions"""
    return await controller.cleanup_executions(max_age_hours)