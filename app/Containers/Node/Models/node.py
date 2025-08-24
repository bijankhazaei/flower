from sqlalchemy import Column, String, Text, JSON, Enum
from app.Ship.Parents.model import BaseModel
import enum

class NodeType(enum.Enum):
    INPUT = "input"
    OUTPUT = "output"
    PROCESSOR = "processor"
    CONDITION = "condition"
    LOOP = "loop"

class Node(BaseModel):
    __tablename__ = "nodes"
    
    name = Column(String(255), nullable=False)
    type = Column(Enum(NodeType), nullable=False)
    category = Column(String(100))
    config = Column(JSON)  # Node configuration
    inputs = Column(JSON)  # Input schema
    outputs = Column(JSON)  # Output schema
    code = Column(Text)  # Executable code