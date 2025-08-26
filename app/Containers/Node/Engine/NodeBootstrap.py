from app.Containers.Node.Engine.BaseNode import node_registry
from app.Containers.Node.Types.BasicNodes import (
    InputNode, OutputNode, TextProcessorNode, ConditionalNode
)
from app.Containers.Node.Types.IONodes import TextInputNode, FileInputNode, TextOutputNode, FileOutputNode
from app.Containers.Node.Types.DataProcessingNodes import JSONProcessorNode, TextSplitterNode, DataTransformerNode
from app.Containers.Node.Types.LogicNodes import ConditionalRouterNode, MergeNode, DelayNode


def register_basic_nodes():
    """Register all basic node types"""
    node_registry.register(InputNode)
    node_registry.register(OutputNode)
    node_registry.register(TextProcessorNode)
    node_registry.register(ConditionalNode)

def register_io_nodes():
    """Register I/O node types"""
    node_registry.register(TextInputNode)
    node_registry.register(FileInputNode)
    node_registry.register(TextOutputNode)
    node_registry.register(FileOutputNode)

def register_data_processing_nodes():
    """Register data processing node types"""
    node_registry.register(JSONProcessorNode)
    node_registry.register(TextSplitterNode)
    node_registry.register(DataTransformerNode)

def register_logic_nodes():
    """Register logic node types"""
    node_registry.register(ConditionalRouterNode)
    node_registry.register(MergeNode)
    node_registry.register(DelayNode)

def bootstrap_nodes():
    """Bootstrap the node system"""
    register_basic_nodes()
    register_io_nodes()
    register_data_processing_nodes()
    register_logic_nodes()
    print(f"Registered {len(node_registry.list_nodes())} node types")
    print(f"Available nodes: {', '.join(node_registry.list_nodes())}")