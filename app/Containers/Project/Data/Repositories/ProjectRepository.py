from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.Ship.Parents.Repositories.Repository import Repository
from app.Containers.Project.Models.Project import Project, ProjectStatus
from app.Containers.Project.Models.UserProject import UserProject


class ProjectRepository(Repository):
    def __init__(self, db: Session):
        super().__init__(db, Project)

    def find_by_owner(self, owner_id: str) -> List[Project]:
        return self.db.query(Project).filter(Project.owner_id == owner_id).all()

    def find_user_projects(self, user_id: str) -> List[Project]:
        return (
            self.db.query(Project)
            .join(UserProject)
            .filter(UserProject.user_id == user_id)
            .options(joinedload(Project.owner))
            .all()
        )

    def find_with_users(self, project_id: str) -> Optional[Project]:
        return (
            self.db.query(Project)
            .options(joinedload(Project.users))
            .filter(Project.id == project_id)
            .first()
        )

    def update_status(self, project_id: str, status: ProjectStatus) -> Optional[Project]:
        project = self.find(project_id)
        if project:
            project.status = status
            self.db.commit()
            self.db.refresh(project)
        return project