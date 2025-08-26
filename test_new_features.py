#!/usr/bin/env python3
"""
Test script for new Flower features:
- Custom node upload
- Compilation caching
- New node library (I/O, Data Processing, Logic nodes)
- Template management
"""

import asyncio
import json
import requests
import time

BASE_URL = "http://localhost:8000/api"

def test_node_library():
    """Test the expanded node library"""
    print("=== Testing Node Library ===")
    
    response = requests.get(f"{BASE_URL}/nodes/types")
    if response.status_code == 200:
        node_types = response.json()
        print(f"Available node types: {len(node_types)}")
        for node_type in node_types:
            print(f"  - {node_type}")
        
        # Test specific new nodes
        new_nodes = ["TextInputNode", "JSONProcessorNode", "ConditionalRouterNode", "MergeNode"]
        for node in new_nodes:
            if node in node_types:
                print(f"✅ {node} registered successfully")
            else:
                print(f"❌ {node} not found")
    else:
        print(f"❌ Failed to get node types: {response.status_code}")

def test_compilation_caching():
    """Test compilation caching performance"""
    print("\n=== Testing Compilation Caching ===")
    
    flow_definition = {
        "nodes": [
            {"id": "input1", "type": "TextInputNode", "config": {"default_text": "Hello"}},
            {"id": "transform1", "type": "DataTransformerNode", "config": {"operation": "uppercase"}},
            {"id": "output1", "type": "TextOutputNode", "config": {"output_key": "result"}}
        ],
        "connections": [
            {"source": "input1", "target": "transform1"},
            {"source": "transform1", "target": "output1"}
        ]
    }
    
    # First compilation (should be slow)
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/compiler/compile", json={"flow_definition": flow_definition})
    first_compile_time = time.time() - start_time
    
    if response.status_code == 200:
        print(f"✅ First compilation: {first_compile_time:.3f}s")
        
        # Second compilation (should be faster due to caching)
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/compiler/compile", json={"flow_definition": flow_definition})
        second_compile_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Second compilation: {second_compile_time:.3f}s")
            if "Used cached compilation result" in result.get("warnings", []):
                print("✅ Cache hit detected!")
            else:
                print("⚠️ Cache miss - might be expected on first run")
        else:
            print(f"❌ Second compilation failed: {response.status_code}")
    else:
        print(f"❌ First compilation failed: {response.status_code}")

def test_template_management():
    """Test template creation and retrieval"""
    print("\n=== Testing Template Management ===")
    
    # Create a template
    template_data = {
        "name": "Text Processing Template",
        "description": "A simple text processing workflow",
        "category": "Text Processing",
        "flow_definition": {
            "nodes": [
                {"id": "input1", "type": "TextInputNode", "config": {"placeholder": "Enter text"}},
                {"id": "split1", "type": "TextSplitterNode", "config": {"split_type": "words"}},
                {"id": "merge1", "type": "MergeNode", "config": {"separator": " | "}}
            ],
            "connections": [
                {"source": "input1", "target": "split1"},
                {"source": "split1", "target": "merge1"}
            ]
        },
        "is_public": True
    }
    
    response = requests.post(f"{BASE_URL}/templates/", json=template_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Template created: {result['name']}")
        template_id = result['id']
        
        # Get templates
        response = requests.get(f"{BASE_URL}/templates/")
        if response.status_code == 200:
            templates = response.json()
            print(f"✅ Retrieved {len(templates)} templates")
            for template in templates:
                print(f"  - {template['name']} ({template['category']})")
        else:
            print(f"❌ Failed to get templates: {response.status_code}")
    else:
        print(f"❌ Template creation failed: {response.status_code}")

def test_custom_node_upload():
    """Test custom node upload functionality"""
    print("\n=== Testing Custom Node Upload ===")
    
    custom_node_code = '''
from typing import Dict, Any, List
from app.Containers.Node.Engine.BaseNode import BaseNode, NodeMetadata, NodePort, NodeParameter, DataType, ExecutionContext

class CustomGreetingNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Custom Greeting",
            description="A custom node that creates personalized greetings",
            category="Custom"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="name", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="greeting", data_type=DataType.TEXT)]
    
    @property
    def parameters(self) -> List[NodeParameter]:
        return [
            NodeParameter(name="greeting_type", data_type=DataType.TEXT, required=False, default="Hello")
        ]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        name = context.inputs.get("name", "World")
        greeting_type = self.get_parameter("greeting_type")
        greeting = f"{greeting_type}, {name}!"
        return {"greeting": greeting}
'''
    
    upload_data = {
        "node_name": "CustomGreetingNode",
        "node_code": custom_node_code
    }
    
    response = requests.post(f"{BASE_URL}/nodes/upload", json=upload_data)
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"✅ Custom node uploaded: {result['node_type']}")
            
            # Verify it's in the registry
            response = requests.get(f"{BASE_URL}/nodes/types")
            if response.status_code == 200:
                node_types = response.json()
                if "CustomGreetingNode" in node_types:
                    print("✅ Custom node registered successfully")
                else:
                    print("❌ Custom node not found in registry")
        else:
            print(f"❌ Custom node upload failed: {result.get('message')}")
    else:
        print(f"❌ Custom node upload request failed: {response.status_code}")

def test_complex_flow():
    """Test a complex flow using new nodes"""
    print("\n=== Testing Complex Flow with New Nodes ===")
    
    complex_flow = {
        "nodes": [
            {"id": "text_input", "type": "TextInputNode", "config": {"default_text": "Hello, World! This is a test."}},
            {"id": "splitter", "type": "TextSplitterNode", "config": {"split_type": "words"}},
            {"id": "json_proc", "type": "JSONProcessorNode", "config": {"operation": "stringify"}},
            {"id": "condition", "type": "ConditionalRouterNode", "config": {"condition_type": "contains", "expected_value": "test"}},
            {"id": "merger", "type": "MergeNode", "config": {"merge_type": "concat", "separator": " -> "}},
            {"id": "output", "type": "TextOutputNode", "config": {"output_key": "final_result"}}
        ],
        "connections": [
            {"source": "text_input", "target": "splitter"},
            {"source": "text_input", "target": "condition"},
            {"source": "condition", "target": "merger"},
            {"source": "splitter", "target": "merger"},
            {"source": "merger", "target": "output"}
        ]
    }
    
    # Compile the flow
    response = requests.post(f"{BASE_URL}/compiler/compile", json={"flow_definition": complex_flow})
    if response.status_code == 200:
        print("✅ Complex flow compiled successfully")
        
        # Execute the flow
        response = requests.post(f"{BASE_URL}/compiler/execute", json={
            "flow_definition": complex_flow,
            "inputs": {"text": "Hello, World! This is a test."}
        })
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Complex flow executed successfully")
            print(f"   Execution status: {result.get('status')}")
            if result.get('results'):
                print(f"   Results: {result['results']}")
        else:
            print(f"❌ Complex flow execution failed: {response.status_code}")
    else:
        print(f"❌ Complex flow compilation failed: {response.status_code}")

def main():
    """Run all tests"""
    print("🌸 Flower New Features Test Suite")
    print("=" * 50)
    
    try:
        test_node_library()
        test_compilation_caching()
        test_template_management()
        test_custom_node_upload()
        test_complex_flow()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flower API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")

if __name__ == "__main__":
    main()