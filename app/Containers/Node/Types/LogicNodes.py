import asyncio
from typing import Dict, Any, List
from app.Containers.Node.Engine.BaseNode import BaseNode, NodeMetadata, NodePort, NodeParameter, DataType, ExecutionContext

class ConditionalRouterNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Conditional Router",
            description="Route data based on conditional logic",
            category="Logic"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [
            NodePort(name="input", data_type=DataType.TEXT),
            NodePort(name="condition_value", data_type=DataType.TEXT)
        ]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [
            NodePort(name="true_output", data_type=DataType.TEXT),
            NodePort(name="false_output", data_type=DataType.TEXT)
        ]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="condition_type", data_type=DataType.TEXT, required=True,
                         default="equals", description="equals, contains, greater_than, less_than"),
            NodeParameter(name="expected_value", data_type=DataType.TEXT, required=True, default="")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input_data = context.inputs.get("input", "")
        condition_value = context.inputs.get("condition_value", input_data)
        condition_type = self.get_parameter("condition_type")
        expected_value = self.get_parameter("expected_value")
        
        result = False
        if condition_type == "equals":
            result = condition_value == expected_value
        elif condition_type == "contains":
            result = expected_value in condition_value
        elif condition_type == "greater_than":
            try:
                result = float(condition_value) > float(expected_value)
            except:
                result = False
        elif condition_type == "less_than":
            try:
                result = float(condition_value) < float(expected_value)
            except:
                result = False
        
        if result:
            return {"true_output": input_data, "false_output": ""}
        else:
            return {"true_output": "", "false_output": input_data}

class MergeNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Merge Node",
            description="Merge multiple inputs into a single output",
            category="Logic"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [
            NodePort(name="input1", data_type=DataType.TEXT),
            NodePort(name="input2", data_type=DataType.TEXT),
            NodePort(name="input3", data_type=DataType.TEXT, required=False)
        ]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="merged", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="separator", data_type=DataType.TEXT, required=False, default=" "),
            NodeParameter(name="merge_type", data_type=DataType.TEXT, required=True,
                         default="concat", description="concat, json_array, json_object")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input1 = context.inputs.get("input1", "")
        input2 = context.inputs.get("input2", "")
        input3 = context.inputs.get("input3", "")
        separator = self.get_parameter("separator")
        merge_type = self.get_parameter("merge_type")
        
        inputs = [inp for inp in [input1, input2, input3] if inp]
        
        if merge_type == "concat":
            result = separator.join(inputs)
        elif merge_type == "json_array":
            import json
            result = json.dumps(inputs)
        elif merge_type == "json_object":
            import json
            result = json.dumps({f"input{i+1}": inp for i, inp in enumerate(inputs)})
        else:
            result = separator.join(inputs)
        
        return {"merged": result}

class DelayNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Delay Node",
            description="Add a delay before passing data through",
            category="Logic"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="input", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="output", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="delay_seconds", data_type=DataType.INTEGER, required=True, default=1)
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input_data = context.inputs.get("input", "")
        delay_seconds = self.get_parameter("delay_seconds")
        
        await asyncio.sleep(delay_seconds)
        return {"output": input_data}