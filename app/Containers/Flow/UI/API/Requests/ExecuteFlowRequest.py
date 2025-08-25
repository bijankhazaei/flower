from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class ExecuteFlowRequest(BaseModel):
    """Request model for flow execution"""
    
    flow_definition: Dict[str, Any] = Field(
        ...,
        description="Flow definition containing nodes and connections"
    )
    
    inputs: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Input data for the flow execution"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "flow_definition": {
                    "id": "sample_flow",
                    "name": "Sample Flow",
                    "nodes": [
                        {
                            "id": "input_1",
                            "type": "InputNode",
                            "parameters": {
                                "input_key": "text"
                            }
                        },
                        {
                            "id": "processor_1",
                            "type": "TextProcessorNode",
                            "parameters": {
                                "operation": "uppercase"
                            },
                            "input_mappings": {
                                "text": {
                                    "source_node": "input_1",
                                    "source_output": "output"
                                }
                            }
                        },
                        {
                            "id": "output_1",
                            "type": "OutputNode",
                            "parameters": {
                                "output_key": "result"
                            },
                            "input_mappings": {
                                "input": {
                                    "source_node": "processor_1",
                                    "source_output": "processed_text"
                                }
                            }
                        }
                    ],
                    "connections": [
                        {
                            "source": "input_1",
                            "target": "processor_1"
                        },
                        {
                            "source": "processor_1",
                            "target": "output_1"
                        }
                    ]
                },
                "inputs": {
                    "text": "hello world"
                }
            }
        }