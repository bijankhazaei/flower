#!/usr/bin/env python3
"""
Test script for all API endpoints
"""

import asyncio
import json
from fastapi.testclient import TestClient
from app.Ship.Engine.app import create_app


def test_api_endpoints():
    """Test all API endpoints"""
    
    # Create test client
    app = create_app()
    client = TestClient(app)
    
    print("🧪 Testing API endpoints...")
    
    # Test health check
    print("\n1. Testing health check...")
    response = client.get("/health")
    assert response.status_code == 200
    print("✅ Health check passed")
    
    # Test node types listing
    print("\n2. Testing node types listing...")
    response = client.get("/api/nodes/types")
    assert response.status_code == 200
    data = response.json()
    assert "node_types" in data
    assert data["count"] > 0
    print(f"✅ Found {data['count']} node types")
    
    # Test specific node info
    print("\n3. Testing specific node info...")
    response = client.get("/api/nodes/types/TextProcessorNode")
    assert response.status_code == 200
    data = response.json()
    assert data["metadata"]["name"] == "Text Processor"
    print("✅ Node info retrieved successfully")
    
    # Test node validation
    print("\n4. Testing node validation...")
    node_config = {
        "node_type": "TextProcessorNode",
        "config": {
            "id": "test_processor",
            "parameters": {
                "operation": "uppercase"
            }
        }
    }
    response = client.post("/api/nodes/validate", json=node_config)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True
    print("✅ Node validation passed")
    
    # Test flow validation
    print("\n5. Testing flow validation...")
    flow_def = {
        "flow_definition": {
            "id": "test_flow",
            "name": "Test Flow",
            "nodes": [
                {
                    "id": "input_1",
                    "type": "InputNode",
                    "parameters": {"input_key": "text"}
                },
                {
                    "id": "output_1",
                    "type": "OutputNode",
                    "parameters": {"output_key": "result"},
                    "input_mappings": {
                        "input": {
                            "source_node": "input_1",
                            "source_output": "output"
                        }
                    }
                }
            ],
            "connections": [
                {"source": "input_1", "target": "output_1"}
            ]
        }
    }
    response = client.post("/api/compiler/validate", json=flow_def)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True
    print("✅ Flow validation passed")
    
    # Test flow compilation
    print("\n6. Testing flow compilation...")
    response = client.post("/api/compiler/compile", json=flow_def)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "code" in data
    print("✅ Flow compilation passed")
    
    # Test flow execution
    print("\n7. Testing flow execution...")
    execute_request = {
        **flow_def,
        "inputs": {"text": "hello world"}
    }
    response = client.post("/api/compiler/execute", json=execute_request)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert "execution_id" in data
    execution_id = data["execution_id"]
    print(f"✅ Flow execution completed: {execution_id}")
    
    # Test execution monitoring
    print("\n8. Testing execution monitoring...")
    response = client.get(f"/api/executions/{execution_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["execution_id"] == execution_id
    assert data["status"] == "completed"
    print("✅ Execution monitoring passed")
    
    # Test executions listing
    print("\n9. Testing executions listing...")
    response = client.get("/api/executions/")
    assert response.status_code == 200
    data = response.json()
    assert "executions" in data
    assert data["count"] >= 1
    print(f"✅ Found {data['count']} executions")
    
    print("\n🎉 All API tests passed!")


if __name__ == "__main__":
    test_api_endpoints()