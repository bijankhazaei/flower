from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.Ship.Engine.database import get_db
from app.Containers.User.Data.Repositories.UserRepository import UserRepository
from app.Containers.User.Tasks.CreateUserTask import CreateUserTask
from app.Containers.User.UI.API.Requests.CreateUserRequest import CreateUserRequest
from app.Containers.User.UI.API.Requests.UpdateUserRequest import UpdateUserRequest
from app.Containers.User.UI.API.Transformers.UserTransformer import UserTransformer

router = APIRouter(prefix="/users", tags=["users"])

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

@router.get("/")
async def get_users(user_repo: UserRepository = Depends(get_user_repository)):
    users = user_repo.get_all()
    return [UserTransformer.transform(user) for user in users]

@router.post("/")
async def create_user(
    request: CreateUserRequest,
    user_repo: UserRepository = Depends(get_user_repository)
):
    # Check if email already exists
    if user_repo.get_by_email(request.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    task = CreateUserTask(user_repo)
    user = task.run(request.dict())
    return UserTransformer.transform(user)

@router.get("/{user_id}")
async def get_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)):
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserTransformer.transform(user)

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    request: UpdateUserRequest,
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = user_repo.update(user_id, request.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserTransformer.transform(user)

@router.delete("/{user_id}")
async def delete_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)):
    if not user_repo.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}