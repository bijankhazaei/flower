#!/usr/bin/env python3
"""
Test script to verify user management functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_user_management():
    print("🌸 Testing Flower User Management System")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    
    # Test get all users (should be empty initially)
    print("\n2. Testing get all users...")
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Get users successful. Found {len(users)} users")
        else:
            print(f"❌ Get users failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get users error: {e}")
        return False
    
    # Test create user
    print("\n3. Testing create user...")
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "role": "user",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/users", json=user_data)
        if response.status_code == 200:
            created_user = response.json()
            user_id = created_user["id"]
            print(f"✅ User created successfully. ID: {user_id}")
        else:
            print(f"❌ Create user failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Create user error: {e}")
        return False
    
    # Test get user by ID
    print("\n4. Testing get user by ID...")
    try:
        response = requests.get(f"{BASE_URL}/api/users/{user_id}")
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Get user by ID successful: {user['name']}")
        else:
            print(f"❌ Get user by ID failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get user by ID error: {e}")
        return False
    
    # Test update user
    print("\n5. Testing update user...")
    update_data = {
        "name": "Updated Test User",
        "role": "admin"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/users/{user_id}", json=update_data)
        if response.status_code == 200:
            updated_user = response.json()
            print(f"✅ User updated successfully: {updated_user['name']}")
        else:
            print(f"❌ Update user failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Update user error: {e}")
        return False
    
    # Test delete user
    print("\n6. Testing delete user...")
    try:
        response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
        if response.status_code == 200:
            print("✅ User deleted successfully")
        else:
            print(f"❌ Delete user failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Delete user error: {e}")
        return False
    
    print("\n🎉 All user management tests passed!")
    return True

if __name__ == "__main__":
    test_user_management()