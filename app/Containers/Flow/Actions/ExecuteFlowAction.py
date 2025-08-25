from typing import Dict, Any
from app.Ship.Parents.action import Action
from app.Containers.Execution.Engine.FlowExecutor import flow_executor, FlowDefinition, FlowExecution


class ExecuteFlowAction(Action):
    """Action to execute a flow"""
    
    async def run(self, flow_definition: Dict[str, Any], inputs: Dict[str, Any] = None) -> FlowExecution:
        """Execute a flow with given inputs"""
        
        # Convert dict to FlowDefinition
        flow_def = FlowDefinition(
            id=flow_definition.get('id', 'temp_flow'),
            name=flow_definition.get('name', 'Temporary Flow'),
            nodes=flow_definition.get('nodes', []),
            connections=flow_definition.get('connections', []),
            metadata=flow_definition.get('metadata', {})
        )
        
        # Execute the flow
        execution = await flow_executor.execute_flow(flow_def, inputs)
        
        return execution