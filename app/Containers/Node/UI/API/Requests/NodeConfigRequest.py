from pydantic import BaseModel, Field
from typing import Dict, Any


class NodeConfigRequest(BaseModel):
    """Request model for node configuration validation"""
    
    node_type: str = Field(
        ...,
        description="Type of node to validate"
    )
    
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Node configuration to validate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "node_type": "TextProcessorNode",
                "config": {
                    "id": "processor_1",
                    "parameters": {
                        "operation": "uppercase"
                    }
                }
            }
        }