# 🌸 Flower - Visual Flow Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

A next-generation visual flow builder designed to address Langflow's architectural limitations through modern software engineering practices. Built with FastAPI and Porto architecture for scalability, maintainability, and performance.

## ✨ Features

- 🎨 **Visual Flow Editor** - Drag-and-drop interface for building AI workflows
- ⚡ **High Performance** - Async/await throughout with parallel node execution
- 🏗️ **Porto Architecture** - Modular, testable, and maintainable codebase
- 🔌 **Extensible Nodes** - Plugin-based system for custom node types
- 🚀 **Real-time Compilation** - Visual flows compiled to executable Python code
- 📊 **Execution Monitoring** - Track flow runs with detailed metrics
- 🔒 **Type Safety** - Full Pydantic validation and SQLAlchemy models
- 🐳 **Docker Ready** - Complete containerized deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (recommended)

### Option 1: Docker (Recommended)
```bash
git clone https://github.com/yourusername/flower.git
cd flower
./run.sh
```

### Option 2: Local Development
```bash
git clone https://github.com/yourusername/flower.git
cd flower
pip install -r requirements.txt
uvicorn main:app --reload
```

Access the application:
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Backend**: http://localhost:8000

### Default Login
- **Email**: admin@flower.com
- **Password**: admin123

## 🏗️ Architecture

Flower uses the **Porto Architecture** pattern for clean, scalable code organization:

```
app/
├── Containers/           # Business modules
│   ├── Flow/            # Flow management
│   ├── Node/            # Node system
│   ├── Execution/       # Flow execution
│   └── User/            # Authentication
└── Ship/                # Framework layer
    ├── Engine/          # Core application
    ├── Parents/         # Base classes
    └── Middlewares/     # HTTP middlewares
```

## 📚 API Documentation

### Flow Compilation
```bash
# Compile visual flow to Python code
POST /api/compiler/compile
{
  "flow_definition": {
    "nodes": [...],
    "connections": [...]
  }
}

# Execute flow with inputs
POST /api/compiler/execute
{
  "flow_definition": {...},
  "inputs": {"text": "hello world"}
}
```

### Node Management
```bash
# List available node types
GET /api/nodes/types

# Get node information
GET /api/nodes/types/TextProcessorNode

# Validate node configuration
POST /api/nodes/validate
```

### Execution Monitoring
```bash
# Get execution details
GET /api/executions/{execution_id}

# List recent executions
GET /api/executions/
```

## 🔌 Creating Custom Nodes

```python
from app.Containers.Node.Engine.BaseNode import BaseNode, NodeMetadata, NodePort, DataType

class MyCustomNode(BaseNode):
    @property
    def metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="My Custom Node",
            description="Does something amazing",
            category="Custom"
        )
    
    @property
    def input_ports(self) -> List[NodePort]:
        return [NodePort(name="input", data_type=DataType.TEXT)]
    
    @property
    def output_ports(self) -> List[NodePort]:
        return [NodePort(name="output", data_type=DataType.TEXT)]
    
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        input_text = context.inputs.get("input", "")
        # Your custom logic here
        return {"output": f"Processed: {input_text}"}

# Register the node
from app.Containers.Node.Engine.BaseNode import node_registry
node_registry.register(MyCustomNode)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Test the flow system
python test_flow_system.py

# Test API endpoints
python test_api_endpoints.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 **Report Bugs** - Found an issue? Let us know!
- 💡 **Feature Requests** - Have ideas? We'd love to hear them!
- 🔧 **Code Contributions** - Submit PRs for bug fixes or new features
- 📖 **Documentation** - Help improve our docs
- 🎨 **Node Library** - Create new node types for the community
- 🧪 **Testing** - Add tests to improve coverage

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following our [coding standards](CONTRIBUTING.md#coding-standards)
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Submit a pull request

### Priority Areas for Contributors

- 🎨 **Visual Editor Frontend** - React/Vue.js canvas editor
- 🤖 **LLM Nodes** - OpenAI, Anthropic, local LLM integrations
- 🔗 **Connectors** - Database, API, file system integrations
- 📊 **Monitoring** - Enhanced execution analytics
- 🔒 **Security** - Authentication and authorization improvements

## 📋 Roadmap

### Phase 1: Foundation ✅
- [x] Flow compiler and execution engine
- [x] Node system and registry
- [x] REST API endpoints
- [x] Basic node library

### Phase 2: Visual Editor 🔄
- [ ] Canvas-based flow editor
- [ ] Real-time collaboration
- [ ] Flow templates and sharing

### Phase 3: Advanced Features
- [ ] LLM integration nodes
- [ ] Advanced monitoring and analytics
- [ ] Plugin marketplace
- [ ] Enterprise features

## 🆚 Why Flower?

| Feature | Flower | Langflow |
|---------|--------|----------|
| Architecture | Porto (modular) | Monolithic |
| Performance | Async/parallel | Synchronous |
| Type Safety | Full Pydantic | Limited |
| Testing | Built-in framework | Manual |
| Extensibility | Plugin system | Hardcoded |
| Code Quality | Clean separation | Tightly coupled |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Langflow's vision of visual AI workflows
- Built with modern Python ecosystem tools
- Community-driven development approach

## 📞 Support

- 📖 **Documentation**: [docs.flower.dev](https://docs.flower.dev)
- 💬 **Discord**: [Join our community](https://discord.gg/flower)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/flower/issues)
- 📧 **Email**: support@flower.dev

---

**⭐ Star this repo if you find it useful!**

Made with ❤️ by the Flower community