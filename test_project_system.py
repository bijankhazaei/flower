#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.Containers.Project.Models.Project import Project, ProjectStatus
from app.Containers.Project.Models.UserProject import UserProject, UserProjectRole
from app.Containers.Project.Data.Repositories.ProjectRepository import ProjectRepository
from app.Containers.Project.Actions.CreateProjectAction import CreateProjectAction
from app.Ship.Engine.database import SessionLocal
import uuid

def test_project_system():
    print("🧪 Testing Project Management System")
    print("=" * 50)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Test 1: Create a project
        print("\n1. Testing Project Creation")
        project_data = {
            "name": "Test Project",
            "description": "A test project for validation",
            "owner_id": uuid.uuid4(),
            "status": ProjectStatus.ACTIVE
        }
        
        action = CreateProjectAction()
        project = action.run(project_data, db)
        
        print(f"✅ Project created: {project.name} (ID: {project.id})")
        print(f"   Status: {project.status.value}")
        print(f"   Owner ID: {project.owner_id}")
        
        # Test 2: Repository operations
        print("\n2. Testing Repository Operations")
        repository = ProjectRepository(db)
        
        # Find by ID
        found_project = repository.find_by_id(project.id)
        print(f"✅ Found project by ID: {found_project.name}")
        
        # Get all projects
        all_projects = repository.get_all()
        print(f"✅ Total projects in database: {len(all_projects)}")
        
        # Test 3: Update project
        print("\n3. Testing Project Update")
        updated_project = repository.update(project.id, {
            "description": "Updated description"
        })
        print(f"✅ Project updated: {updated_project.description}")
        
        # Test 4: User-Project association
        print("\n4. Testing User-Project Association")
        user_id = uuid.uuid4()
        success = repository.add_user_to_project(
            project.id, 
            user_id, 
            UserProjectRole.EDITOR
        )
        print(f"✅ User added to project: {success}")
        
        # Get project users
        project_users = repository.get_project_users(project.id)
        print(f"✅ Project has {len(project_users)} users")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    test_project_system()