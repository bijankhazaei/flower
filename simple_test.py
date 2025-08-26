#!/usr/bin/env python3

import requests
import json

def test_running_server():
    """Test the running server"""
    
    base_url = "http://localhost:8022"
    
    try:
        # Test health check
        print("Testing health check...")
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test node types
        print("\nTesting node types...")
        response = requests.get(f"{base_url}/api/nodes/types")
        print(f"Node types: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data.get('count', 0)} node types")
        
        # Test flow compilation
        print("\nTesting flow compilation...")
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
        
        response = requests.post(f"{base_url}/api/compiler/compile", json=flow_def)
        print(f"Flow compilation: {response.status_code}")
        if response.status_code == 200:
            print("✅ Compilation successful")
        else:
            print(f"❌ Compilation failed: {response.text}")
        
        # Test flow execution
        print("\nTesting flow execution...")
        execute_request = {
            **flow_def,
            "inputs": {"text": "hello world"}
        }
        
        response = requests.post(f"{base_url}/api/compiler/execute", json=execute_request)
        print(f"Flow execution: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Execution successful: {data.get('execution_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Outputs: {data.get('outputs')}")
        else:
            print(f"❌ Execution failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Start it with: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_running_server()