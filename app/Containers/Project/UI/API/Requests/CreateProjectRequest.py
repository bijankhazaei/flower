from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, max_length=1000, description="Project description")
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Project settings")