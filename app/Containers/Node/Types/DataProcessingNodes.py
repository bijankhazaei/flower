import json
import csv
from io import StringIO
from typing import Dict, Any, List
from app.Containers.Node.Engine.BaseNode import BaseNode, NodeMetadata, NodePort, NodeParameter, DataType, ExecutionContext

class JSONProcessorNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="JSON Processor",
            description="Parse, manipulate, and format JSON data",
            category="Data Processing"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="json_input", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="result", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="operation", data_type=DataType.TEXT, required=True, 
                         default="parse", description="parse, stringify, extract_key"),
            NodeParameter(name="key_path", data_type=DataType.TEXT, required=False, default="")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        json_input = context.inputs.get("json_input", "{}")
        operation = self.get_parameter("operation")
        key_path = self.get_parameter("key_path")
        
        try:
            if operation == "parse":
                parsed = json.loads(json_input)
                return {"result": str(parsed)}
            elif operation == "stringify":
                return {"result": json.dumps(json.loads(json_input), indent=2)}
            elif operation == "extract_key" and key_path:
                parsed = json.loads(json_input)
                keys = key_path.split('.')
                result = parsed
                for key in keys:
                    result = result[key]
                return {"result": str(result)}
            else:
                return {"result": json_input}
        except Exception as e:
            raise Exception(f"JSON processing failed: {str(e)}")

class TextSplitterNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Text Splitter",
            description="Split text into chunks based on various criteria",
            category="Data Processing"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="text", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="chunks", data_type=DataType.LIST)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="split_type", data_type=DataType.TEXT, required=True, 
                         default="lines", description="lines, words, chars, delimiter"),
            NodeParameter(name="delimiter", data_type=DataType.TEXT, required=False, default=","),
            NodeParameter(name="chunk_size", data_type=DataType.INTEGER, required=False, default=1000)
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        text = context.inputs.get("text", "")
        split_type = self.get_parameter("split_type")
        delimiter = self.get_parameter("delimiter")
        chunk_size = self.get_parameter("chunk_size")
        
        if split_type == "lines":
            chunks = text.split('\n')
        elif split_type == "words":
            chunks = text.split()
        elif split_type == "chars":
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        elif split_type == "delimiter":
            chunks = text.split(delimiter)
        else:
            chunks = [text]
        
        return {"chunks": chunks}

class DataTransformerNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Data Transformer",
            description="Transform data using various operations",
            category="Data Processing"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="data", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="transformed", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="operation", data_type=DataType.TEXT, required=True,
                         default="uppercase", description="uppercase, lowercase, trim, replace"),
            NodeParameter(name="find_text", data_type=DataType.TEXT, required=False, default=""),
            NodeParameter(name="replace_text", data_type=DataType.TEXT, required=False, default="")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        data = context.inputs.get("data", "")
        operation = self.get_parameter("operation")
        find_text = self.get_parameter("find_text")
        replace_text = self.get_parameter("replace_text")
        
        if operation == "uppercase":
            result = data.upper()
        elif operation == "lowercase":
            result = data.lower()
        elif operation == "trim":
            result = data.strip()
        elif operation == "replace" and find_text:
            result = data.replace(find_text, replace_text)
        else:
            result = data
        
        return {"transformed": result}