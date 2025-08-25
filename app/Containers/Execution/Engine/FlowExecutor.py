from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import uuid
from datetime import datetime

from app.Containers.Node.Engine.BaseNode import BaseNode, ExecutionContext, ExecutionResult, node_registry


class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class FlowExecution:
    id: str
    flow_id: str
    status: ExecutionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    node_results: Dict[str, ExecutionResult] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FlowDefinition:
    id: str
    name: str
    nodes: List[Dict[str, Any]]
    connections: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


class FlowExecutor:
    """Executes compiled flows with async node processing"""
    
    def __init__(self):
        self.active_executions: Dict[str, FlowExecution] = {}
    
    async def execute_flow(self, flow_definition: FlowDefinition, inputs: Dict[str, Any] = None) -> FlowExecution:
        """Execute a flow definition"""
        execution_id = str(uuid.uuid4())
        execution = FlowExecution(
            id=execution_id,
            flow_id=flow_definition.id,
            status=ExecutionStatus.PENDING,
            start_time=datetime.now(),
            inputs=inputs or {}
        )
        
        self.active_executions[execution_id] = execution
        
        try:
            execution.status = ExecutionStatus.RUNNING
            
            # Build execution graph
            execution_graph = self._build_execution_graph(flow_definition)
            
            # Execute nodes
            await self._execute_nodes(execution, execution_graph, flow_definition)
            
            execution.status = ExecutionStatus.COMPLETED
            execution.end_time = datetime.now()
            
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.end_time = datetime.now()
        
        return execution
    
    def _build_execution_graph(self, flow_definition: FlowDefinition) -> Dict[str, Set[str]]:
        """Build dependency graph for execution order"""
        graph = {node['id']: set() for node in flow_definition.nodes}
        
        # Build dependencies (reverse of connections)
        for connection in flow_definition.connections:
            source = connection['source']
            target = connection['target']
            graph[target].add(source)
        
        return graph
    
    async def _execute_nodes(self, execution: FlowExecution, graph: Dict[str, Set[str]], flow_definition: FlowDefinition):
        """Execute nodes in topological order with parallel processing"""
        nodes_by_id = {node['id']: node for node in flow_definition.nodes}
        completed_nodes = set()
        node_outputs = {}
        
        while len(completed_nodes) < len(flow_definition.nodes):
            # Find nodes ready to execute (all dependencies completed)
            ready_nodes = []
            for node_id, dependencies in graph.items():
                if node_id not in completed_nodes and dependencies.issubset(completed_nodes):
                    ready_nodes.append(node_id)
            
            if not ready_nodes:
                raise RuntimeError("Circular dependency detected in flow")
            
            # Execute ready nodes in parallel
            tasks = []
            for node_id in ready_nodes:
                node_def = nodes_by_id[node_id]
                task = self._execute_single_node(execution, node_def, node_outputs)
                tasks.append((node_id, task))
            
            # Wait for all tasks to complete
            for node_id, task in tasks:
                try:
                    result = await task
                    execution.node_results[node_id] = result
                    
                    if result.success:
                        node_outputs[node_id] = result.outputs
                        completed_nodes.add(node_id)
                    else:
                        raise RuntimeError(f"Node {node_id} failed: {result.error}")
                        
                except Exception as e:
                    raise RuntimeError(f"Node {node_id} execution failed: {str(e)}")
        
        # Set final outputs
        execution.outputs = self._collect_flow_outputs(flow_definition, node_outputs)
    
    async def _execute_single_node(self, execution: FlowExecution, node_def: Dict[str, Any], node_outputs: Dict[str, Dict[str, Any]]) -> ExecutionResult:
        """Execute a single node"""
        node_type = node_def.get('type')
        node_id = node_def['id']
        
        # Create node instance
        node_instance = node_registry.create_node(node_type, node_def)
        if not node_instance:
            return ExecutionResult(
                success=False,
                error=f"Unknown node type: {node_type}"
            )
        
        # Prepare inputs from connected nodes
        node_inputs = self._prepare_node_inputs(node_def, node_outputs, execution.inputs)
        
        # Create execution context
        context = ExecutionContext(
            flow_id=execution.flow_id,
            node_id=node_id,
            execution_id=execution.id,
            inputs=node_inputs,
            parameters=node_def.get('parameters', {}),
            metadata=node_def.get('metadata', {})
        )
        
        # Execute node
        return await node_instance.execute(context)
    
    def _prepare_node_inputs(self, node_def: Dict[str, Any], node_outputs: Dict[str, Dict[str, Any]], flow_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare inputs for a node from connected nodes and flow inputs"""
        inputs = {}
        
        # Add flow-level inputs if this is an input node
        if node_def.get('type') == 'InputNode':
            inputs.update(flow_inputs)
        
        # Add inputs from connected nodes
        input_mappings = node_def.get('input_mappings', {})
        for input_name, mapping in input_mappings.items():
            source_node = mapping.get('source_node')
            source_output = mapping.get('source_output')
            
            if source_node in node_outputs and source_output in node_outputs[source_node]:
                inputs[input_name] = node_outputs[source_node][source_output]
        
        return inputs
    
    def _collect_flow_outputs(self, flow_definition: FlowDefinition, node_outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Collect final outputs from output nodes"""
        outputs = {}
        
        for node in flow_definition.nodes:
            if node.get('type') == 'OutputNode':
                node_id = node['id']
                if node_id in node_outputs:
                    outputs.update(node_outputs[node_id])
        
        return outputs
    
    def get_execution(self, execution_id: str) -> Optional[FlowExecution]:
        """Get execution by ID"""
        return self.active_executions.get(execution_id)
    
    def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running execution"""
        execution = self.active_executions.get(execution_id)
        if execution and execution.status == ExecutionStatus.RUNNING:
            execution.status = ExecutionStatus.CANCELLED
            execution.end_time = datetime.now()
            return True
        return False
    
    def list_executions(self) -> List[FlowExecution]:
        """List all executions"""
        return list(self.active_executions.values())
    
    def cleanup_completed_executions(self, max_age_hours: int = 24) -> int:
        """Clean up old completed executions"""
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        to_remove = []
        
        for execution_id, execution in self.active_executions.items():
            if (execution.status in [ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.CANCELLED] 
                and execution.end_time 
                and execution.end_time.timestamp() < cutoff_time):
                to_remove.append(execution_id)
        
        for execution_id in to_remove:
            del self.active_executions[execution_id]
        
        return len(to_remove)


# Global executor instance
flow_executor = FlowExecutor()