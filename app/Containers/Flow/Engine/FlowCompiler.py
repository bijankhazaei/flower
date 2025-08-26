from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import ast
import json
from dataclasses import dataclass
from app.Containers.Flow.Engine.CompilationCache import CompilationCache


@dataclass
class CompilationResult:
    success: bool
    code: Optional[str] = None
    errors: List[str] = None
    warnings: List[str] = None


class FlowCompiler(ABC):
    """Base class for converting visual flows to executable code"""
    
    def __init__(self, use_cache: bool = True):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.cache = CompilationCache() if use_cache else None
    
    def compile(self, flow_definition: Dict[str, Any]) -> CompilationResult:
        """Main compilation entry point"""
        self.errors.clear()
        self.warnings.clear()
        
        try:
            # Check cache first
            if self.cache:
                cached_code = self.cache.get(flow_definition)
                if cached_code:
                    return CompilationResult(
                        success=True,
                        code=cached_code,
                        warnings=["Used cached compilation result"]
                    )
            
            # Validate flow structure
            if not self._validate_flow(flow_definition):
                return CompilationResult(success=False, errors=self.errors)
            
            # Convert to AST
            flow_ast = self._json_to_ast(flow_definition)
            
            # Generate code
            code = self._generate_code(flow_ast)
            
            # Cache result
            if self.cache:
                self.cache.set(flow_definition, code)
            
            return CompilationResult(
                success=True,
                code=code,
                warnings=self.warnings
            )
            
        except Exception as e:
            self.errors.append(f"Compilation failed: {str(e)}")
            return CompilationResult(success=False, errors=self.errors)
    
    def _validate_flow(self, flow_definition: Dict[str, Any]) -> bool:
        """Validate flow structure and dependencies"""
        required_fields = ['nodes', 'connections']
        
        for field in required_fields:
            if field not in flow_definition:
                self.errors.append(f"Missing required field: {field}")
                return False
        
        nodes = flow_definition.get('nodes', [])
        connections = flow_definition.get('connections', [])
        
        # Validate nodes
        node_ids = set()
        for node in nodes:
            if 'id' not in node:
                self.errors.append("Node missing required 'id' field")
                return False
            
            if node['id'] in node_ids:
                self.errors.append(f"Duplicate node id: {node['id']}")
                return False
            
            node_ids.add(node['id'])
        
        # Validate connections
        for conn in connections:
            if 'source' not in conn or 'target' not in conn:
                self.errors.append("Connection missing source or target")
                return False
            
            if conn['source'] not in node_ids or conn['target'] not in node_ids:
                self.errors.append("Connection references non-existent node")
                return False
        
        return True
    
    @abstractmethod
    def _json_to_ast(self, flow_definition: Dict[str, Any]) -> ast.AST:
        """Convert flow JSON to Python AST"""
        pass
    
    @abstractmethod
    def _generate_code(self, flow_ast: ast.AST) -> str:
        """Generate executable code from AST"""
        pass


class PythonFlowCompiler(FlowCompiler):
    """Python-specific flow compiler implementation"""
    
    def _json_to_ast(self, flow_definition: Dict[str, Any]) -> ast.Module:
        """Convert flow to Python AST"""
        nodes = flow_definition['nodes']
        connections = flow_definition['connections']
        
        # Create module
        module = ast.Module(body=[], type_ignores=[])
        
        # Add imports
        imports = self._generate_imports(nodes)
        module.body.extend(imports)
        
        # Add flow function
        flow_func = self._create_flow_function(nodes, connections)
        module.body.append(flow_func)
        
        return module
    
    def _generate_imports(self, nodes: List[Dict]) -> List[ast.stmt]:
        """Generate import statements based on node types"""
        imports = [
            ast.Import(names=[ast.alias(name='asyncio', asname=None)]),
            ast.ImportFrom(
                module='typing',
                names=[ast.alias(name='Dict', asname=None), ast.alias(name='Any', asname=None)],
                level=0
            )
        ]
        
        # Add node-specific imports
        node_types = {node.get('type') for node in nodes}
        for node_type in node_types:
            if node_type:
                imports.append(
                    ast.ImportFrom(
                        module=f'app.Containers.Node.Types.{node_type}',
                        names=[ast.alias(name=node_type, asname=None)],
                        level=0
                    )
                )
        
        return imports
    
    def _create_flow_function(self, nodes: List[Dict], connections: List[Dict]) -> ast.AsyncFunctionDef:
        """Create the main flow execution function"""
        # Build execution order
        execution_order = self._build_execution_order(nodes, connections)
        
        # Create function body
        body = []
        
        # Initialize nodes
        for node in nodes:
            node_init = self._create_node_initialization(node)
            body.append(node_init)
        
        # Execute nodes in order
        for node_id in execution_order:
            node_exec = self._create_node_execution(node_id)
            body.append(node_exec)
        
        # Return statement
        return_stmt = ast.Return(
            value=ast.Dict(
                keys=[ast.Constant(value='status')],
                values=[ast.Constant(value='completed')]
            )
        )
        body.append(return_stmt)
        
        return ast.AsyncFunctionDef(
            name='execute_flow',
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg='inputs', annotation=ast.Name(id='Dict', ctx=ast.Load()))],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]
            ),
            body=body,
            decorator_list=[],
            returns=ast.Name(id='Dict', ctx=ast.Load())
        )
    
    def _build_execution_order(self, nodes: List[Dict], connections: List[Dict]) -> List[str]:
        """Build topological execution order"""
        # Simple topological sort
        in_degree = {node['id']: 0 for node in nodes}
        graph = {node['id']: [] for node in nodes}
        
        for conn in connections:
            graph[conn['source']].append(conn['target'])
            in_degree[conn['target']] += 1
        
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            node_id = queue.pop(0)
            result.append(node_id)
            
            for neighbor in graph[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    def _create_node_initialization(self, node: Dict) -> ast.Assign:
        """Create node initialization statement"""
        node_type = node.get('type', 'BaseNode')
        node_id = node['id']
        
        return ast.Assign(
            targets=[ast.Name(id=f'node_{node_id}', ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id=node_type, ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(
                        arg='config',
                        value=ast.Dict(
                            keys=[ast.Constant(value=k) for k in node.get('config', {}).keys()],
                            values=[ast.Constant(value=v) for v in node.get('config', {}).values()]
                        )
                    )
                ]
            )
        )
    
    def _create_node_execution(self, node_id: str) -> ast.Assign:
        """Create node execution statement"""
        return ast.Assign(
            targets=[ast.Name(id=f'result_{node_id}', ctx=ast.Store())],
            value=ast.Await(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id=f'node_{node_id}', ctx=ast.Load()),
                        attr='execute',
                        ctx=ast.Load()
                    ),
                    args=[ast.Name(id='inputs', ctx=ast.Load())],
                    keywords=[]
                )
            )
        )
    
    def _generate_code(self, flow_ast: ast.Module) -> str:
        """Generate Python code from AST"""
        import astor
        return astor.to_source(flow_ast)