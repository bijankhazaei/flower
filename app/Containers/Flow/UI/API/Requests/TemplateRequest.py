from pydantic import BaseModel
from typing import Optional, Dict, Any

class CreateTemplateRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    category: Optional[str] = None
    flow_definition: Dict[str, Any]
    is_public: Optional[bool] = False

class UpdateTemplateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    flow_definition: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None