from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.Ship.Engine.database import get_db
from app.Containers.User.Models.User import User
from app.Containers.Project.Actions.CreateProjectAction import CreateProjectAction
from app.Containers.Project.Actions.GetUserProjectsAction import GetUserProjectsAction
from app.Containers.Project.UI.API.Requests.CreateProjectRequest import CreateProjectRequest
from app.Containers.Project.Models.Project import ProjectStatus
from typing import List
import uuid

router = APIRouter(prefix="/api/projects", tags=["projects"])

# TODO: Implement proper authentication
def get_current_user() -> User:
    # Placeholder - implement proper JWT authentication
    pass


@router.post("/", response_model=dict)
async def create_project(
    request: CreateProjectRequest,
    db: Session = Depends(get_db)
):
    try:
        action = CreateProjectAction()
        project = action.run(request.dict(), db)
        
        return {
            "id": str(project.id),
            "name": project.name,
            "description": project.description,
            "status": project.status.value,
            "owner_id": str(project.owner_id),
            "created_at": project.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[dict])
async def list_projects(
    db: Session = Depends(get_db)
):
    # TODO: Filter by user permissions
    from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
    
    project_repository = ProjectRepository(db)
    projects = project_repository.get_all()
    
    return [
        {
            "id": str(project.id),
            "name": project.name,
            "description": project.description,
            "status": project.status.value,
            "owner_id": str(project.owner_id),
            "created_at": project.created_at.isoformat()
        }
        for project in projects
    ]


@router.get("/{project_id}", response_model=dict)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
    
    project_repository = ProjectRepository(db)
    project = project_repository.find_by_id(uuid.UUID(project_id))
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": str(project.id),
        "name": project.name,
        "description": project.description,
        "status": project.status.value,
        "owner_id": str(project.owner_id),
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat()
    }


# TODO: Add update, delete, and status management endpoints