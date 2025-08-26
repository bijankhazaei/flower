#!/usr/bin/env python3
"""
Test script for enhanced Flower system
Tests the new project management, user management, and flow management features
"""

import requests
import json

BASE_URL = "http://localhost:8022"

def test_login():
    """Test user login"""
    response = requests.post(f"{BASE_URL}/api/users/login", json={
        "email": "admin@flower.com",
        "password": "admin123"
    })
    
    if response.status_code == 200:
        print("✅ Login successful")
        return response.json().get("access_token")
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_project_management(token):
    """Test project CRUD operations"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create project
    project_data = {
        "name": "Test Project",
        "description": "A test project for the enhanced system",
        "settings": {"theme": "dark"}
    }
    
    response = requests.post(f"{BASE_URL}/api/projects/", json=project_data, headers=headers)
    
    if response.status_code == 200:
        project = response.json()
        print(f"✅ Project created: {project['name']} (ID: {project['id']})")
        
        # List projects
        response = requests.get(f"{BASE_URL}/api/projects/", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Found {len(projects)} projects")
        
        return project['id']
    else:
        print(f"❌ Project creation failed: {response.text}")
        return None

def test_flow_management(token, project_id):
    """Test flow management within projects"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create flow
    flow_data = {
        "name": "Test Flow",
        "description": "A test flow",
        "definition": {
            "nodes": [
                {"id": "input_1", "type": "TextInput", "config": {"placeholder": "Enter text"}},
                {"id": "output_1", "type": "TextOutput", "config": {}}
            ],
            "connections": [{"source": "input_1", "target": "output_1"}]
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/projects/{project_id}/flows/",
        params=flow_data,
        headers=headers
    )
    
    if response.status_code == 200:
        flow = response.json()
        print(f"✅ Flow created: {flow['name']} (ID: {flow['id']})")
        return flow['id']
    else:
        print(f"❌ Flow creation failed: {response.text}")
        return None

def test_user_management(token):
    """Test user management features"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # List users
    response = requests.get(f"{BASE_URL}/api/users/", headers=headers)
    
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Found {len(users)} users")
        
        if users:
            user_id = users[0]['id']
            # Test user activation (should already be active)
            response = requests.post(f"{BASE_URL}/api/users/{user_id}/activate", headers=headers)
            if response.status_code == 200:
                print("✅ User activation endpoint works")
    else:
        print(f"❌ User listing failed: {response.text}")

def main():
    print("🌸 Testing Enhanced Flower System")
    print("=" * 40)
    
    # Test login
    token = test_login()
    if not token:
        return
    
    # Test project management
    project_id = test_project_management(token)
    if not project_id:
        return
    
    # Test flow management
    flow_id = test_flow_management(token, project_id)
    
    # Test user management
    test_user_management(token)
    
    print("\n🎉 Enhanced system testing completed!")

if __name__ == "__main__":
    main()