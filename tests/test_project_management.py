import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Ship.Parents.Models.Model import Base
from app.Ship.Engine.app import create_app
from app.Ship.Engine.Database import get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_project(client):
    # Login first
    login_response = client.post("/api/users/login", json={
        "email": "admin@flower.com",
        "password": "admin123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create project
    response = client.post("/api/projects/", json={
        "name": "Test Project",
        "description": "Test Description"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "Test Description"

def test_list_projects(client):
    # Login and create project first
    login_response = client.post("/api/users/login", json={
        "email": "admin@flower.com",
        "password": "admin123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # List projects
    response = client.get("/api/projects/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)