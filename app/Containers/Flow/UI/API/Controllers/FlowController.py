from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.Ship.Engine.Database import get_db
from app.Ship.Engine.Auth import get_current_user
from app.Containers.User.Models.User import User
from app.Containers.Flow.Data.Repositories.FlowRepository import FlowRepository
from app.Containers.Flow.Models.Flow import Flow, FlowStatus
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository

router = APIRouter(prefix="/api/projects/{project_id}/flows", tags=["flows"])


@router.post("/", response_model=dict)
def create_flow(
    project_id: str,
    name: str,
    definition: dict,
    description: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify project access
    project_repository = ProjectRepository(db)
    project = project_repository.find(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    flow_repository = FlowRepository(db)
    flow = flow_repository.create({
        "project_id": project_id,
        "name": name,
        "description": description,
        "definition": definition,
        "created_by": str(current_user.id)
    })
    
    return {
        "id": str(flow.id),
        "name": flow.name,
        "description": flow.description,
        "status": flow.status.value,
        "version": flow.version,
        "created_at": flow.created_at.isoformat()
    }


@router.get("/", response_model=List[dict])
def list_flows(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    flow_repository = FlowRepository(db)
    flows = flow_repository.find_by_project(project_id)
    
    return [
        {
            "id": str(flow.id),
            "name": flow.name,
            "description": flow.description,
            "status": flow.status.value,
            "version": flow.version,
            "created_at": flow.created_at.isoformat()
        }
        for flow in flows
    ]


@router.get("/{flow_id}", response_model=dict)
def get_flow(
    project_id: str,
    flow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    flow_repository = FlowRepository(db)
    flow = flow_repository.find(flow_id)
    
    if not flow or str(flow.project_id) != project_id:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    return {
        "id": str(flow.id),
        "name": flow.name,
        "description": flow.description,
        "definition": flow.definition,
        "status": flow.status.value,
        "version": flow.version,
        "created_at": flow.created_at.isoformat(),
        "updated_at": flow.updated_at.isoformat()
    }


@router.put("/{flow_id}/status", response_model=dict)
def update_flow_status(
    project_id: str,
    flow_id: str,
    status: FlowStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    flow_repository = FlowRepository(db)
    flow = flow_repository.update_status(flow_id, status)
    
    if not flow or str(flow.project_id) != project_id:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    return {
        "id": str(flow.id),
        "status": flow.status.value,
        "updated_at": flow.updated_at.isoformat()
    }