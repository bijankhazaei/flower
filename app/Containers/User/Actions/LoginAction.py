from app.Ship.Parents.action import Action
from app.Containers.User.Tasks.AuthenticateUserTask import AuthenticateUserTask
from app.Containers.User.Models.User import User
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

class LoginAction(Action):
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self):
        self.authenticate_task = AuthenticateUserTask()

    def run(self, email: str, password: str) -> dict:
        user = self.authenticate_task.run(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token = self.create_access_token(data={"sub": user.email})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.value
            }
        }

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt