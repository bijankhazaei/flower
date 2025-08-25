from typing import Dict, Any, List
from app.Containers.Node.Engine.BaseNode import (
    BaseNode, NodeMetadata, NodePort, NodeParameter, 
    DataType, NodeType, ExecutionContext
)


class InputNode(BaseNode):
    """Node for receiving flow inputs"""
    
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Input",
            description="Receives input data for the flow",
            category="Input/Output",
            tags=["input", "data"]
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return []
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [
            NodePort(
                name="output",
                data_type=DataType.ANY,
                description="Flow input data"
            )
        ]
    
    @property
    def parameters_schema(self) -> List[NodeParameter]:
        return [
            NodeParameter(
                name="input_key",
                data_type=DataType.TEXT,
                description="Key to extract from flow inputs",
                default_value="input"
            )
        ]
    
    @property
    def node_type(self) -> NodeType:
        return NodeType.INPUT
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input_key = self.get_parameter("input_key", "input")
        input_value = context.inputs.get(input_key)
        
        return {
            "output": input_value
        }


class OutputNode(BaseNode):
    """Node for producing flow outputs"""
    
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Output",
            description="Produces output data from the flow",
            category="Input/Output",
            tags=["output", "data"]
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [
            NodePort(
                name="input",
                data_type=DataType.ANY,
                description="Data to output"
            )
        ]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [
            NodePort(
                name="result",
                data_type=DataType.ANY,
                description="Output result"
            )
        ]
    
    @property
    def parameters_schema(self) -> List[NodeParameter]:
        return [
            NodeParameter(
                name="output_key",
                data_type=DataType.TEXT,
                description="Key for the output data",
                default_value="result"
            )
        ]
    
    @property
    def node_type(self) -> NodeType:
        return NodeType.OUTPUT
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input_data = context.inputs.get("input")
        output_key = self.get_parameter("output_key", "result")
        
        return {
            output_key: input_data
        }


class TextProcessorNode(BaseNode):
    """Node for basic text processing"""
    
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Text Processor",
            description="Performs basic text processing operations",
            category="Text Processing",
            tags=["text", "processing", "transform"]
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [
            NodePort(
                name="text",
                data_type=DataType.TEXT,
                description="Input text to process"
            )
        ]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [
            NodePort(
                name="processed_text",
                data_type=DataType.TEXT,
                description="Processed text output"
            )
        ]
    
    @property
    def parameters_schema(self) -> List[NodeParameter]:
        return [
            NodeParameter(
                name="operation",
                data_type=DataType.TEXT,
                description="Text operation to perform",
                default_value="uppercase",
                options=["uppercase", "lowercase", "title", "strip", "reverse"]
            )
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        text = context.inputs.get("text", "")
        operation = self.get_parameter("operation", "uppercase")
        
        if operation == "uppercase":
            result = text.upper()
        elif operation == "lowercase":
            result = text.lower()
        elif operation == "title":
            result = text.title()
        elif operation == "strip":
            result = text.strip()
        elif operation == "reverse":
            result = text[::-1]
        else:
            result = text
        
        return {
            "processed_text": result
        }


class ConditionalNode(BaseNode):
    """Node for conditional logic"""
    
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Conditional",
            description="Routes data based on conditions",
            category="Logic",
            tags=["condition", "logic", "routing"]
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [
            NodePort(
                name="input",
                data_type=DataType.ANY,
                description="Input data to evaluate"
            ),
            NodePort(
                name="condition_value",
                data_type=DataType.ANY,
                description="Value to compare against",
                required=False
            )
        ]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [
            NodePort(
                name="true_output",
                data_type=DataType.ANY,
                description="Output when condition is true",
                required=False
            ),
            NodePort(
                name="false_output",
                data_type=DataType.ANY,
                description="Output when condition is false",
                required=False
            )
        ]
    
    @property
    def parameters_schema(self) -> List[NodeParameter]:
        return [
            NodeParameter(
                name="condition_type",
                data_type=DataType.TEXT,
                description="Type of condition to evaluate",
                default_value="equals",
                options=["equals", "not_equals", "greater_than", "less_than", "contains", "is_empty"]
            ),
            NodeParameter(
                name="condition_value",
                data_type=DataType.TEXT,
                description="Value to compare against",
                default_value="",
                required=False
            )
        ]
    
    @property
    def node_type(self) -> NodeType:
        return NodeType.CONDITION
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input_data = context.inputs.get("input")
        condition_type = self.get_parameter("condition_type", "equals")
        condition_value = context.inputs.get("condition_value") or self.get_parameter("condition_value")
        
        result = self._evaluate_condition(input_data, condition_type, condition_value)
        
        if result:
            return {"true_output": input_data}
        else:
            return {"false_output": input_data}
    
    def _evaluate_condition(self, input_data: Any, condition_type: str, condition_value: Any) -> bool:
        """Evaluate the condition"""
        if condition_type == "equals":
            return input_data == condition_value
        elif condition_type == "not_equals":
            return input_data != condition_value
        elif condition_type == "greater_than":
            try:
                return float(input_data) > float(condition_value)
            except (ValueError, TypeError):
                return False
        elif condition_type == "less_than":
            try:
                return float(input_data) < float(condition_value)
            except (ValueError, TypeError):
                return False
        elif condition_type == "contains":
            return str(condition_value) in str(input_data)
        elif condition_type == "is_empty":
            return not input_data or (isinstance(input_data, str) and input_data.strip() == "")
        
        return False