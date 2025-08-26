from typing import Dict, Any
from app.Ship.Parents.Actions.Action import Action
from app.Containers.Flow.Engine.FlowCompiler import PythonFlowCompiler, CompilationResult
from app.Containers.Flow.Tasks.ValidateFlowTask import ValidateFlowTask


class CompileFlowAction(Action):
    """Action to compile a visual flow to executable code"""
    
    def __init__(self):
        self.compiler = PythonFlowCompiler()
        self.validate_task = ValidateFlowTask()
    
    async def run(self, flow_definition: Dict[str, Any]) -> CompilationResult:
        """Compile flow definition to executable code"""
        
        # Validate flow first
        validation_result = await self.validate_task.run(flow_definition)
        if not validation_result['valid']:
            return CompilationResult(
                success=False,
                errors=validation_result['errors']
            )
        
        # Compile the flow
        compilation_result = self.compiler.compile(flow_definition)
        
        return compilation_result