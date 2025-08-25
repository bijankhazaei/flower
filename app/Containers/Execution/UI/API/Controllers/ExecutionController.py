from fastapi import HTTPException
from typing import Dict, Any, List, Optional
from app.Containers.Execution.Engine.FlowExecutor import flow_executor


class ExecutionController:
    """Controller for execution monitoring"""
    
    async def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """Get execution details by ID"""
        try:
            execution = flow_executor.get_execution(execution_id)
            
            if not execution:
                raise HTTPException(status_code=404, detail=f"Execution '{execution_id}' not found")
            
            return {
                "execution_id": execution.id,
                "flow_id": execution.flow_id,
                "status": execution.status.value,
                "start_time": execution.start_time.isoformat(),
                "end_time": execution.end_time.isoformat() if execution.end_time else None,
                "inputs": execution.inputs,
                "outputs": execution.outputs,
                "error": execution.error,
                "node_results": {
                    node_id: {
                        "success": result.success,
                        "outputs": result.outputs,
                        "error": result.error,
                        "execution_time": result.execution_time
                    }
                    for node_id, result in execution.node_results.items()
                },
                "metadata": execution.metadata
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get execution: {str(e)}")
    
    async def list_executions(self, limit: int = 50, status: Optional[str] = None) -> Dict[str, Any]:
        """List recent executions"""
        try:
            executions = flow_executor.list_executions()
            
            # Filter by status if provided
            if status:
                executions = [e for e in executions if e.status.value == status]
            
            # Sort by start time (newest first) and limit
            executions.sort(key=lambda x: x.start_time, reverse=True)
            executions = executions[:limit]
            
            return {
                "executions": [
                    {
                        "execution_id": execution.id,
                        "flow_id": execution.flow_id,
                        "status": execution.status.value,
                        "start_time": execution.start_time.isoformat(),
                        "end_time": execution.end_time.isoformat() if execution.end_time else None,
                        "error": execution.error
                    }
                    for execution in executions
                ],
                "count": len(executions)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list executions: {str(e)}")
    
    async def cancel_execution(self, execution_id: str) -> Dict[str, Any]:
        """Cancel a running execution"""
        try:
            success = flow_executor.cancel_execution(execution_id)
            
            if not success:
                raise HTTPException(status_code=400, detail="Execution cannot be cancelled or not found")
            
            return {
                "success": True,
                "message": f"Execution {execution_id} cancelled"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to cancel execution: {str(e)}")
    
    async def cleanup_executions(self, max_age_hours: int = 24) -> Dict[str, Any]:
        """Clean up old completed executions"""
        try:
            cleaned_count = flow_executor.cleanup_completed_executions(max_age_hours)
            
            return {
                "cleaned_count": cleaned_count,
                "message": f"Cleaned up {cleaned_count} old executions"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to cleanup executions: {str(e)}")