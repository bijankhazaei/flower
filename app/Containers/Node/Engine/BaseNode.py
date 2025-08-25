from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass, field
from enum import Enum
import asyncio


class NodeType(Enum):
    INPUT = "input"
    OUTPUT = "output"
    PROCESSOR = "processor"
    CONDITION = "condition"
    LOOP = "loop"


class DataType(Enum):
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    JSON = "json"
    FILE = "file"
    ANY = "any"


@dataclass
class NodePort:
    name: str
    data_type: DataType
    required: bool = True
    description: str = ""


@dataclass
class NodeParameter:
    name: str
    data_type: DataType
    default_value: Any = None
    required: bool = True
    description: str = ""
    options: List[Any] = field(default_factory=list)


@dataclass
class NodeMetadata:
    name: str
    description: str
    category: str
    version: str = "1.0.0"
    author: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class ExecutionContext:
    flow_id: str
    node_id: str
    execution_id: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    success: bool
    outputs: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseNode(ABC):
    """Abstract base class for all node types"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.node_id = self.config.get('id', '')
        self.parameters = self.config.get('parameters', {})
        self._validate_parameters()
    
    @property
    @abstractmethod
    def metadata(self) -> NodeMetadata:
        """Node metadata including name, description, etc."""
        pass
    
    @property
    @abstractmethod
    def input_ports(self) -> List[NodePort]:
        """Define input ports for this node"""
        pass
    
    @property
    @abstractmethod
    def output_ports(self) -> List[NodePort]:
        """Define output ports for this node"""
        pass
    
    @property
    @abstractmethod
    def parameters_schema(self) -> List[NodeParameter]:
        """Define configurable parameters for this node"""
        pass
    
    @property
    def node_type(self) -> NodeType:
        """Default node type - can be overridden"""
        return NodeType.PROCESSOR
    
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """Execute the node with given context"""
        import time
        start_time = time.time()
        
        try:
            # Validate inputs
            validation_result = self._validate_inputs(context.inputs)
            if not validation_result.success:
                return ExecutionResult(
                    success=False,
                    error=validation_result.error,
                    execution_time=time.time() - start_time
                )
            
            # Execute node logic
            outputs = await self._execute_logic(context)
            
            # Validate outputs
            output_validation = self._validate_outputs(outputs)
            if not output_validation.success:
                return ExecutionResult(
                    success=False,
                    error=output_validation.error,
                    execution_time=time.time() - start_time
                )
            
            return ExecutionResult(
                success=True,
                outputs=outputs,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    @abstractmethod
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        """Implement the core node logic"""
        pass
    
    def _validate_parameters(self) -> None:
        """Validate node parameters against schema"""
        schema = {param.name: param for param in self.parameters_schema}
        
        for param_name, param_def in schema.items():
            if param_def.required and param_name not in self.parameters:
                if param_def.default_value is not None:
                    self.parameters[param_name] = param_def.default_value
                else:
                    raise ValueError(f"Required parameter '{param_name}' not provided")
            
            # Type validation would go here
    
    def _validate_inputs(self, inputs: Dict[str, Any]) -> ExecutionResult:
        """Validate input data against input ports schema"""
        for port in self.input_ports:
            if port.required and port.name not in inputs:
                return ExecutionResult(
                    success=False,
                    error=f"Required input '{port.name}' not provided"
                )
            
            # Type validation would go here
        
        return ExecutionResult(success=True)
    
    def _validate_outputs(self, outputs: Dict[str, Any]) -> ExecutionResult:
        """Validate output data against output ports schema"""
        for port in self.output_ports:
            if port.required and port.name not in outputs:
                return ExecutionResult(
                    success=False,
                    error=f"Required output '{port.name}' not generated"
                )
        
        return ExecutionResult(success=True)
    
    def get_parameter(self, name: str, default: Any = None) -> Any:
        """Get parameter value with optional default"""
        return self.parameters.get(name, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize node to dictionary"""
        return {
            'id': self.node_id,
            'metadata': {
                'name': self.metadata.name,
                'description': self.metadata.description,
                'category': self.metadata.category,
                'version': self.metadata.version,
                'author': self.metadata.author,
                'tags': self.metadata.tags
            },
            'type': self.node_type.value,
            'input_ports': [
                {
                    'name': port.name,
                    'data_type': port.data_type.value,
                    'required': port.required,
                    'description': port.description
                }
                for port in self.input_ports
            ],
            'output_ports': [
                {
                    'name': port.name,
                    'data_type': port.data_type.value,
                    'required': port.required,
                    'description': port.description
                }
                for port in self.output_ports
            ],
            'parameters_schema': [
                {
                    'name': param.name,
                    'data_type': param.data_type.value,
                    'default_value': param.default_value,
                    'required': param.required,
                    'description': param.description,
                    'options': param.options
                }
                for param in self.parameters_schema
            ],
            'config': self.config
        }


class NodeRegistry:
    """Registry for managing node types"""
    
    def __init__(self):
        self._nodes: Dict[str, Type[BaseNode]] = {}
    
    def register(self, node_class: Type[BaseNode]) -> None:
        """Register a node type"""
        node_name = node_class.__name__
        self._nodes[node_name] = node_class
    
    def get(self, node_type: str) -> Optional[Type[BaseNode]]:
        """Get node class by type name"""
        return self._nodes.get(node_type)
    
    def list_nodes(self) -> List[str]:
        """List all registered node types"""
        return list(self._nodes.keys())
    
    def create_node(self, node_type: str, config: Dict[str, Any] = None) -> Optional[BaseNode]:
        """Create node instance"""
        node_class = self.get(node_type)
        if node_class:
            return node_class(config)
        return None
    
    def get_node_info(self, node_type: str) -> Optional[Dict[str, Any]]:
        """Get node metadata and schema"""
        node_class = self.get(node_type)
        if node_class:
            # Create temporary instance to get metadata
            temp_node = node_class()
            return temp_node.to_dict()
        return None


# Global registry instance
node_registry = NodeRegistry()