from typing import Dict, Any, List
from app.Containers.Node.Engine.BaseNode import BaseNode, NodeMetadata, NodePort, NodeParameter, DataType, ExecutionContext

class TextInputNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Text Input",
            description="Accepts text input from user or flow",
            category="Input/Output"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return []
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="text", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="default_text", data_type=DataType.TEXT, required=False, default=""),
            NodeParameter(name="placeholder", data_type=DataType.TEXT, required=False, default="Enter text...")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input_text = context.inputs.get("text", self.get_parameter("default_text"))
        return {"text": input_text}

class FileInputNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="File Input",
            description="Reads content from a file",
            category="Input/Output"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="file_path", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="content", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="encoding", data_type=DataType.TEXT, required=False, default="utf-8")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        file_path = context.inputs.get("file_path")
        encoding = self.get_parameter("encoding")
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return {"content": content}
        except Exception as e:
            raise Exception(f"Failed to read file: {str(e)}")

class TextOutputNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Text Output",
            description="Outputs text data from the flow",
            category="Input/Output"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="text", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="result", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="output_key", data_type=DataType.TEXT, required=False, default="output")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        text = context.inputs.get("text", "")
        output_key = self.get_parameter("output_key")
        return {"result": text, output_key: text}

class FileOutputNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="File Output",
            description="Writes content to a file",
            category="Input/Output"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [
            NodePort(name="content", data_type=DataType.TEXT),
            NodePort(name="file_path", data_type=DataType.TEXT)
        ]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="success", data_type=DataType.BOOLEAN)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="encoding", data_type=DataType.TEXT, required=False, default="utf-8"),
            NodeParameter(name="append", data_type=DataType.BOOLEAN, required=False, default=False)
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        content = context.inputs.get("content", "")
        file_path = context.inputs.get("file_path")
        encoding = self.get_parameter("encoding")
        append_mode = self.get_parameter("append")
        
        try:
            mode = 'a' if append_mode else 'w'
            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)
            return {"success": True}
        except Exception as e:
            raise Exception(f"Failed to write file: {str(e)}")