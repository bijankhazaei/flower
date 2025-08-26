from typing import List, Optional
from sqlalchemy.orm import Session
from app.Ship.Parents.Repositories.Repository import Repository
from app.Containers.Flow.Models.Flow import Flow, FlowStatus


class FlowRepository(Repository):
    def __init__(self, db: Session):
        super().__init__(db, Flow)

    def find_by_project(self, project_id: str) -> List[Flow]:
        return self.db.query(Flow).filter(Flow.project_id == project_id).all()

    def find_by_status(self, status: FlowStatus) -> List[Flow]:
        return self.db.query(Flow).filter(Flow.status == status).all()

    def update_status(self, flow_id: str, status: FlowStatus) -> Optional[Flow]:
        flow = self.find(flow_id)
        if flow:
            flow.status = status
            self.db.commit()
            self.db.refresh(flow)
        return flow

    def create_version(self, flow_id: str, definition: dict, changes_summary: str = None) -> Optional[Flow]:
        flow = self.find(flow_id)
        if flow:
            flow.version += 1
            flow.definition = definition
            self.db.commit()
            self.db.refresh(flow)
        return flow