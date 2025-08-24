from app.Ship.Parents.task import Task
from app.Containers.User.Models.User import User
from app.Containers.User.Data.Repositories.UserRepository import UserRepository

class CreateUserTask(Task):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def run(self, user_data: dict) -> User:
        return self.user_repository.create(user_data)