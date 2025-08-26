import os
import importlib.util
from typing import Dict, Any
from app.Ship.Parents.Tasks.Task import Task
from app.Containers.Node.Engine.BaseNode import BaseNode, node_registry

class UploadCustomNodeTask(Task):
    def __init__(self):
        self.upload_dir = "app/Containers/Node/Types/Custom"
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def run(self, node_code: str, node_name: str) -> Dict[str, Any]:
        """Upload and register a custom node"""
        try:
            # Save node file
            file_path = os.path.join(self.upload_dir, f"{node_name}.py")
            with open(file_path, 'w') as f:
                f.write(node_code)
            
            # Load and validate node
            spec = importlib.util.spec_from_file_location(node_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find node class
            node_class = getattr(module, node_name, None)
            if not node_class or not issubclass(node_class, BaseNode):
                raise ValueError(f"Invalid node class: {node_name}")
            
            # Register node
            node_registry.register(node_class)
            
            return {
                "success": True,
                "message": f"Node {node_name} uploaded and registered successfully",
                "node_type": node_name
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to upload node: {str(e)}"
            }