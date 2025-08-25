from typing import Dict, Any, List
from app.Ship.Parents.task import Task


class ValidateFlowTask(Task):
    """Task to validate flow definitions"""
    
    async def run(self, flow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Validate flow structure and return validation result"""
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ['nodes', 'connections']
        for field in required_fields:
            if field not in flow_definition:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return {
                'valid': False,
                'errors': errors,
                'warnings': warnings
            }
        
        # Validate nodes
        nodes = flow_definition.get('nodes', [])
        connections = flow_definition.get('connections', [])
        
        node_validation = self._validate_nodes(nodes)
        errors.extend(node_validation['errors'])
        warnings.extend(node_validation['warnings'])
        
        # Validate connections
        connection_validation = self._validate_connections(connections, nodes)
        errors.extend(connection_validation['errors'])
        warnings.extend(connection_validation['warnings'])
        
        # Check for cycles
        cycle_validation = self._check_cycles(nodes, connections)
        errors.extend(cycle_validation['errors'])
        warnings.extend(cycle_validation['warnings'])
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_nodes(self, nodes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Validate node definitions"""
        errors = []
        warnings = []
        node_ids = set()
        
        for i, node in enumerate(nodes):
            # Check required fields
            if 'id' not in node:
                errors.append(f"Node at index {i} missing required 'id' field")
                continue
            
            if 'type' not in node:
                errors.append(f"Node {node['id']} missing required 'type' field")
            
            # Check for duplicate IDs
            if node['id'] in node_ids:
                errors.append(f"Duplicate node ID: {node['id']}")
            else:
                node_ids.add(node['id'])
        
        return {'errors': errors, 'warnings': warnings}
    
    def _validate_connections(self, connections: List[Dict[str, Any]], nodes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Validate connection definitions"""
        errors = []
        warnings = []
        node_ids = {node['id'] for node in nodes}
        
        for i, conn in enumerate(connections):
            # Check required fields
            if 'source' not in conn:
                errors.append(f"Connection at index {i} missing 'source' field")
                continue
            
            if 'target' not in conn:
                errors.append(f"Connection at index {i} missing 'target' field")
                continue
            
            # Check if referenced nodes exist
            if conn['source'] not in node_ids:
                errors.append(f"Connection references non-existent source node: {conn['source']}")
            
            if conn['target'] not in node_ids:
                errors.append(f"Connection references non-existent target node: {conn['target']}")
            
            # Check for self-connections
            if conn['source'] == conn['target']:
                errors.append(f"Self-connection detected on node: {conn['source']}")
        
        return {'errors': errors, 'warnings': warnings}
    
    def _check_cycles(self, nodes: List[Dict[str, Any]], connections: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Check for circular dependencies"""
        errors = []
        warnings = []
        
        # Build adjacency list
        graph = {node['id']: [] for node in nodes}
        for conn in connections:
            if conn['source'] in graph and conn['target'] in graph:
                graph[conn['source']].append(conn['target'])
        
        # DFS to detect cycles
        visited = set()
        rec_stack = set()
        
        def has_cycle(node_id: str) -> bool:
            if node_id in rec_stack:
                return True
            if node_id in visited:
                return False
            
            visited.add(node_id)
            rec_stack.add(node_id)
            
            for neighbor in graph[node_id]:
                if has_cycle(neighbor):
                    return True
            
            rec_stack.remove(node_id)
            return False
        
        for node_id in graph:
            if node_id not in visited:
                if has_cycle(node_id):
                    errors.append("Circular dependency detected in flow")
                    break
        
        return {'errors': errors, 'warnings': warnings}