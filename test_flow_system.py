#!/usr/bin/env python3
"""
Test script for the flow compilation and execution system
"""

import asyncio
import json
from app.Containers.Node.Engine.NodeBootstrap import bootstrap_nodes
from app.Containers.Flow.Actions.CompileFlowAction import CompileFlowAction
from app.Containers.Flow.Actions.ExecuteFlowAction import ExecuteFlowAction


async def test_flow_system():
    """Test the complete flow system"""
    
    # Bootstrap nodes
    print("🔧 Bootstrapping node system...")
    bootstrap_nodes()
    
    # Define a simple test flow
    flow_definition = {
        "id": "test_flow",
        "name": "Test Flow",
        "nodes": [
            {
                "id": "input_1",
                "type": "InputNode",
                "parameters": {
                    "input_key": "text"
                }
            },
            {
                "id": "processor_1", 
                "type": "TextProcessorNode",
                "parameters": {
                    "operation": "uppercase"
                },
                "input_mappings": {
                    "text": {
                        "source_node": "input_1",
                        "source_output": "output"
                    }
                }
            },
            {
                "id": "output_1",
                "type": "OutputNode", 
                "parameters": {
                    "output_key": "result"
                },
                "input_mappings": {
                    "input": {
                        "source_node": "processor_1",
                        "source_output": "processed_text"
                    }
                }
            }
        ],
        "connections": [
            {
                "source": "input_1",
                "target": "processor_1"
            },
            {
                "source": "processor_1", 
                "target": "output_1"
            }
        ]
    }
    
    # Test compilation
    print("\n📝 Testing flow compilation...")
    compile_action = CompileFlowAction()
    compilation_result = await compile_action.run(flow_definition)
    
    if compilation_result.success:
        print("✅ Compilation successful!")
        print("Generated code:")
        print("-" * 50)
        print(compilation_result.code)
        print("-" * 50)
    else:
        print("❌ Compilation failed!")
        print("Errors:", compilation_result.errors)
        return
    
    # Test execution
    print("\n🚀 Testing flow execution...")
    execute_action = ExecuteFlowAction()
    
    test_inputs = {
        "text": "hello world"
    }
    
    execution = await execute_action.run(flow_definition, test_inputs)
    
    print(f"Execution ID: {execution.id}")
    print(f"Status: {execution.status.value}")
    print(f"Inputs: {execution.inputs}")
    print(f"Outputs: {execution.outputs}")
    
    if execution.error:
        print(f"Error: {execution.error}")
    
    # Show node results
    print("\nNode Results:")
    for node_id, result in execution.node_results.items():
        print(f"  {node_id}: {result.success} - {result.outputs}")
        if result.error:
            print(f"    Error: {result.error}")
    
    print("\n🎉 Flow system test completed!")


if __name__ == "__main__":
    asyncio.run(test_flow_system())