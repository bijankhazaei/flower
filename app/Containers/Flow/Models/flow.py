from sqlalchemy import Column, String, Text, JSON, Enum
from app.Ship.Parents.model import BaseModel
import enum

class FlowStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"

class Flow(BaseModel):
    __tablename__ = "flows"
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    definition = Column(JSON)  # Flow graph structure
    status = Column(Enum(FlowStatus), default=FlowStatus.DRAFT)
    version = Column(String(50), default="1.0.0")