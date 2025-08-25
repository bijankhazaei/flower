from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.Containers.Flow.Actions.CompileFlowAction import CompileFlowAction
from app.Containers.Flow.Actions.ExecuteFlowAction import ExecuteFlowAction
from app.Containers.Flow.UI.API.Requests.CompileFlowRequest import CompileFlowRequest
from app.Containers.Flow.UI.API.Requests.ExecuteFlowRequest import ExecuteFlowRequest


class CompilerController:
    """Controller for flow compilation and execution"""
    
    def __init__(self):
        self.compile_action = CompileFlowAction()
        self.execute_action = ExecuteFlowAction()
    
    async def compile_flow(self, request: CompileFlowRequest) -> Dict[str, Any]:
        """Compile a visual flow to executable code"""
        try:
            result = await self.compile_action.run(request.flow_definition)
            
            return {
                "success": result.success,
                "code": result.code,
                "errors": result.errors or [],
                "warnings": result.warnings or []
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Compilation failed: {str(e)}")
    
    async def execute_flow(self, request: ExecuteFlowRequest) -> Dict[str, Any]:
        """Execute a flow with given inputs"""
        try:
            execution = await self.execute_action.run(
                request.flow_definition, 
                request.inputs
            )
            
            return {
                "execution_id": execution.id,
                "status": execution.status.value,
                "outputs": execution.outputs,
                "error": execution.error,
                "start_time": execution.start_time.isoformat(),
                "end_time": execution.end_time.isoformat() if execution.end_time else None,
                "node_results": {
                    node_id: {
                        "success": result.success,
                        "outputs": result.outputs,
                        "error": result.error,
                        "execution_time": result.execution_time
                    }
                    for node_id, result in execution.node_results.items()
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
    
    async def validate_flow(self, request: CompileFlowRequest) -> Dict[str, Any]:
        """Validate a flow definition"""
        try:
            from app.Containers.Flow.Tasks.ValidateFlowTask import ValidateFlowTask
            validate_task = ValidateFlowTask()
            
            result = await validate_task.run(request.flow_definition)
            
            return {
                "valid": result['valid'],
                "errors": result['errors'],
                "warnings": result['warnings']
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")