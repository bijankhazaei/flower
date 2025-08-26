from typing import List, Optional
from sqlalchemy.orm import Session
from app.Containers.User.Models.User import User, UserStatus, UserRole
from app.Ship.Engine.database import get_db

class UserRepository:
    def __init__(self, db: Session = None):
        self.db = db or next(get_db())
    
    def get_all(self) -> List[User]:
        return self.db.query(User).all()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def find_by_email(self, email: str) -> Optional[User]:
        return self.get_by_email(email)
    
    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
    
    def update_status(self, user_id: int, status: str) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            user.status = UserStatus(status)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_role(self, user_id: int, role: UserRole) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            user.role = role
            self.db.commit()
            self.db.refresh(user)
        return user