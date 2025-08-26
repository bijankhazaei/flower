from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.Ship.Engine.Database import get_db
from app.Ship.Engine.Auth import get_current_user
from app.Containers.User.Models.User import User
from app.Containers.Project.Actions.CreateProjectAction import CreateProjectAction
from app.Containers.Project.Tasks.CreateProjectTask import CreateProjectTask
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.UI.API.Requests.CreateProjectRequest import CreateProjectRequest
from app.Containers.Project.Models.Project import Project, ProjectStatus

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("/", response_model=dict)
def create_project(
    request: CreateProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create projects"
        )
    
    project_repository = ProjectRepository(db)
    create_project_task = CreateProjectTask(project_repository)
    create_project_action = CreateProjectAction(create_project_task)
    
    project = create_project_action.run(request, str(current_user.id))
    
    return {
        "id": str(project.id),
        "name": project.name,
        "description": project.description,
        "status": project.status.value,
        "created_at": project.created_at.isoformat()
    }


@router.get("/", response_model=List[dict])
def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_repository = ProjectRepository(db)
    
    if current_user.role.value == "super_admin":
        projects = project_repository.get_all()
    elif current_user.role.value == "admin":
        projects = project_repository.find_by_owner(str(current_user.id))
    else:
        projects = project_repository.find_user_projects(str(current_user.id))
    
    return [
        {
            "id": str(project.id),
            "name": project.name,
            "description": project.description,
            "status": project.status.value,
            "created_at": project.created_at.isoformat()
        }
        for project in projects
    ]


@router.get("/{project_id}", response_model=dict)
def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_repository = ProjectRepository(db)
    project = project_repository.find(project_id)
    
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


@router.put("/{project_id}", response_model=dict)
def update_project(
    project_id: str,
    request: CreateProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_repository = ProjectRepository(db)
    project = project_repository.find(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if current_user.role.value not in ["admin", "super_admin"] and str(project.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    updated_project = project_repository.update(project_id, {
        "name": request.name,
        "description": request.description,
        "settings": request.settings
    })
    
    return {
        "id": str(updated_project.id),
        "name": updated_project.name,
        "description": updated_project.description,
        "status": updated_project.status.value,
        "updated_at": updated_project.updated_at.isoformat()
    }


@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Only admins can delete projects")
    
    project_repository = ProjectRepository(db)
    project = project_repository.find(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_repository.update_status(project_id, ProjectStatus.DELETED)
    
    return {"message": "Project deleted successfully"}


@router.put("/{project_id}/status", response_model=dict)
def update_project_status(
    project_id: str,
    status: ProjectStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Only admins can update project status")
    
    project_repository = ProjectRepository(db)
    project = project_repository.update_status(project_id, status)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": str(project.id),
        "status": project.status.value,
        "updated_at": project.updated_at.isoformat()
    }