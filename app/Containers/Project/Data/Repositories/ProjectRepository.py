from sqlalchemy.orm import Session
from app.Containers.Project.Models.Project import Project, ProjectStatus
from app.Containers.Project.Models.UserProject import UserProject, UserProjectRole
from typing import Optional, List
import uuid

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, project_data: dict) -> Project:
        project = Project(**project_data)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def find_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def find_by_owner(self, owner_id: uuid.UUID) -> List[Project]:
        return self.db.query(Project).filter(Project.owner_id == owner_id).all()
    
    def find_by_user(self, user_id: uuid.UUID) -> List[Project]:
        return self.db.query(Project).join(UserProject).filter(
            UserProject.user_id == user_id
        ).all()
    
    def get_all(self) -> List[Project]:
        return self.db.query(Project).all()
    
    def update(self, project_id: uuid.UUID, project_data: dict) -> Optional[Project]:
        project = self.find_by_id(project_id)
        if project:
            for key, value in project_data.items():
                setattr(project, key, value)
            self.db.commit()
            self.db.refresh(project)
        return project
    
    def delete(self, project_id: uuid.UUID) -> bool:
        project = self.find_by_id(project_id)
        if project:
            project.status = ProjectStatus.DELETED
            self.db.commit()
            return True
        return False
    
    def add_user_to_project(self, project_id: uuid.UUID, user_id: uuid.UUID, role: UserProjectRole = UserProjectRole.VIEWER) -> bool:
        existing = self.db.query(UserProject).filter(
            UserProject.project_id == project_id,
            UserProject.user_id == user_id
        ).first()
        
        if existing:
            return False
        
        user_project = UserProject(
            project_id=project_id,
            user_id=user_id,
            role=role
        )
        self.db.add(user_project)
        self.db.commit()
        return True
    
    def remove_user_from_project(self, project_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        user_project = self.db.query(UserProject).filter(
            UserProject.project_id == project_id,
            UserProject.user_id == user_id
        ).first()
        
        if user_project:
            self.db.delete(user_project)
            self.db.commit()
            return True
        return False
    
    def get_project_users(self, project_id: uuid.UUID) -> List[UserProject]:
        return self.db.query(UserProject).filter(
            UserProject.project_id == project_id
        ).all()