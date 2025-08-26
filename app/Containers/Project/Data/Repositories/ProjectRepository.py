from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_

from app.Ship.Parents.Repositories.Repository import Repository
from app.Containers.Project.Models.Project import Project, ProjectStatus
from app.Containers.Project.Models.UserProject import UserProject, UserProjectRole


class ProjectRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Project)

    async def create_project(self, name: str, description: str, owner_id: str, settings: Dict[str, Any] = None) -> Project:
        """Create a new project"""
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id,
            settings=settings or {}
        )
        self.db_session.add(project)
        self.db_session.commit()
        self.db_session.refresh(project)
        
        # Add owner to user_projects with OWNER role
        user_project = UserProject(
            user_id=owner_id,
            project_id=project.id,
            role=UserProjectRole.OWNER
        )
        self.db_session.add(user_project)
        self.db_session.commit()
        
        return project

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get project by ID with relationships"""
        return self.db_session.query(Project).options(
            joinedload(Project.owner),
            joinedload(Project.users)
        ).filter(Project.id == project_id).first()

    async def get_user_projects(self, user_id: str, status: ProjectStatus = None) -> List[Project]:
        """Get all projects accessible to a user"""
        query = self.db_session.query(Project).join(UserProject).filter(
            UserProject.user_id == user_id
        )
        
        if status:
            query = query.filter(Project.status == status)
        
        return query.options(
            joinedload(Project.owner),
            joinedload(Project.users)
        ).all()

    async def get_owned_projects(self, owner_id: str, status: ProjectStatus = None) -> List[Project]:
        """Get projects owned by a user"""
        query = self.db_session.query(Project).filter(Project.owner_id == owner_id)
        
        if status:
            query = query.filter(Project.status == status)
        
        return query.options(
            joinedload(Project.owner),
            joinedload(Project.users)
        ).all()

    async def update_project(self, project_id: str, updates: Dict[str, Any]) -> Optional[Project]:
        """Update project details"""
        project = await self.get_project_by_id(project_id)
        if not project:
            return None
        
        for key, value in updates.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        self.db_session.commit()
        self.db_session.refresh(project)
        return project

    async def delete_project(self, project_id: str) -> bool:
        """Soft delete project by setting status to DELETED"""
        project = await self.get_project_by_id(project_id)
        if not project:
            return False
        
        project.status = ProjectStatus.DELETED
        self.db_session.commit()
        return True

    async def add_user_to_project(self, project_id: str, user_id: str, role: UserProjectRole = UserProjectRole.VIEWER) -> bool:
        """Add user to project with specified role"""
        # Check if user is already in project
        existing = self.db_session.query(UserProject).filter(
            and_(UserProject.project_id == project_id, UserProject.user_id == user_id)
        ).first()
        
        if existing:
            return False
        
        user_project = UserProject(
            user_id=user_id,
            project_id=project_id,
            role=role
        )
        self.db_session.add(user_project)
        self.db_session.commit()
        return True

    async def remove_user_from_project(self, project_id: str, user_id: str) -> bool:
        """Remove user from project"""
        user_project = self.db_session.query(UserProject).filter(
            and_(UserProject.project_id == project_id, UserProject.user_id == user_id)
        ).first()
        
        if not user_project:
            return False
        
        self.db_session.delete(user_project)
        self.db_session.commit()
        return True

    async def get_project_users(self, project_id: str) -> List[UserProject]:
        """Get all users in a project with their roles"""
        return self.db_session.query(UserProject).options(
            joinedload(UserProject.user)
        ).filter(UserProject.project_id == project_id).all()

    async def user_has_access(self, user_id: str, project_id: str, required_role: UserProjectRole = None) -> bool:
        """Check if user has access to project with optional role requirement"""
        query = self.db_session.query(UserProject).filter(
            and_(UserProject.user_id == user_id, UserProject.project_id == project_id)
        )
        
        if required_role:
            # Define role hierarchy: OWNER > EDITOR > VIEWER
            role_hierarchy = {
                UserProjectRole.VIEWER: 1,
                UserProjectRole.EDITOR: 2,
                UserProjectRole.OWNER: 3
            }
            
            required_level = role_hierarchy.get(required_role, 0)
            user_project = query.first()
            
            if not user_project:
                return False
            
            user_level = role_hierarchy.get(user_project.role, 0)
            return user_level >= required_level
        
        return query.first() is not None