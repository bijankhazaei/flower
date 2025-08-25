from app.Containers.Node.Engine.BaseNode import node_registry
from app.Containers.Node.Types.BasicNodes import (
    InputNode, OutputNode, TextProcessorNode, ConditionalNode
)


def register_basic_nodes():
    """Register all basic node types"""
    node_registry.register(InputNode)
    node_registry.register(OutputNode)
    node_registry.register(TextProcessorNode)
    node_registry.register(ConditionalNode)


def bootstrap_nodes():
    """Bootstrap the node system"""
    register_basic_nodes()
    print(f"Registered {len(node_registry.list_nodes())} node types")
    print(f"Available nodes: {', '.join(node_registry.list_nodes())}")