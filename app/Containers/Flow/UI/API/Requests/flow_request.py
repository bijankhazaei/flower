from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.Containers.Flow.Models.flow import FlowStatus

class CreateFlowRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    definition: Optional[Dict[str, Any]] = None

class UpdateFlowRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    definition: Optional[Dict[str, Any]] = None
    status: Optional[FlowStatus] = None