from sqlalchemy import Column, String, Text, JSON, ForeignKey, Integer, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.Ship.Parents.Models.Model import BaseModel


class FlowVersion(BaseModel):
    __tablename__ = "flow_versions"
    __table_args__ = (UniqueConstraint('flow_id', 'version', name='_flow_version_uc'),)

    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.id'), nullable=False)
    version = Column(Integer, nullable=False)
    definition = Column(JSON, nullable=False)
    changes_summary = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    # Relationships
    flow = relationship("Flow", back_populates="versions")
    created_by_user = relationship("User")

    def __repr__(self):
        return f"<FlowVersion(flow_id={self.flow_id}, version={self.version})>"