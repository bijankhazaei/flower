from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.Containers.Node.Engine.BaseNode import node_registry


class NodeController:
    """Controller for node management"""
    
    async def list_node_types(self) -> Dict[str, Any]:
        """List all available node types"""
        try:
            node_types = []
            
            for node_type in node_registry.list_nodes():
                node_info = node_registry.get_node_info(node_type)
                if node_info:
                    node_types.append(node_info)
            
            return {
                "node_types": node_types,
                "count": len(node_types)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list node types: {str(e)}")
    
    async def get_node_info(self, node_type: str) -> Dict[str, Any]:
        """Get detailed information about a specific node type"""
        try:
            node_info = node_registry.get_node_info(node_type)
            
            if not node_info:
                raise HTTPException(status_code=404, detail=f"Node type '{node_type}' not found")
            
            return node_info
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get node info: {str(e)}")
    
    async def validate_node_config(self, node_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate node configuration"""
        try:
            node_instance = node_registry.create_node(node_type, config)
            
            if not node_instance:
                raise HTTPException(status_code=404, detail=f"Node type '{node_type}' not found")
            
            return {
                "valid": True,
                "node_id": node_instance.node_id,
                "parameters": node_instance.parameters
            }
            
        except ValueError as e:
            return {
                "valid": False,
                "error": str(e)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")