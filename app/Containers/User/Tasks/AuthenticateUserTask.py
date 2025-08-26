from app.Ship.Parents.Tasks.Task import Task
from app.Containers.User.Models.User import User
from app.Containers.User.Data.Repositories.UserRepository import UserRepository
from passlib.context import CryptContext
from typing import Optional

class AuthenticateUserTask(Task):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repository = UserRepository()
    
    def run(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.find_by_email(email)
        if user and self.verify_password(password, user.password_hash):
            return user
        return None
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)