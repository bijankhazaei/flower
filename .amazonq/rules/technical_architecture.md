# Flower Technical Architecture

## 🏗️ Architecture Overview

Flower implements a **Porto Architecture** pattern with a **Hybrid Visual-to-Code** compilation system, providing both ease of use and high performance.

## 📁 Core Directory Structure

```
app/
├── Containers/                 # Business modules (Porto pattern)
│   ├── User/                  # Authentication & user management
│   ├── Project/               # Workspace organization
│   ├── Flow/                  # Flow definitions & compilation
│   ├── Node/                  # Node types & registry
│   └── Execution/             # Flow execution & monitoring
└── Ship/                      # Framework layer
    ├── Engine/                # Core application engine
    ├── Parents/               # Base classes
    └── Middlewares/           # HTTP middlewares
```

## 🔄 Container Architecture (Porto Pattern)

Each container follows consistent structure:

```
Container/
├── Actions/                   # Business operations orchestration
├── Tasks/                    # Specific business logic
├── Models/                   # Business entities (SQLAlchemy)
├── Data/
│   ├── Repositories/         # Data access layer
│   ├── Migrations/           # Database migrations
│   └── Seeders/              # Test data
├── UI/
│   ├── API/
│   │   ├── Controllers/      # HTTP request handlers
│   │   ├── Requests/         # Input validation (Pydantic)
│   │   ├── Transformers/     # Response formatting
│   │   └── Routes/           # API endpoints
│   └── WebSocket/            # Real-time communication
└── Tests/                    # Unit & integration tests
```

## 🔧 Technical Stack

### Backend Core
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: ORM with async support
- **Pydantic**: Data validation and serialization
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage
- **RabbitMQ**: Message broker for async processing

### Frontend Architecture
- **React 18+**: Modern UI framework with TypeScript
- **Zustand**: State management for canvas and app state
- **React Query**: Server state management and caching
- **Tailwind CSS**: Utility-first styling
- **Vite**: Fast build tool and development server

## 🎨 Hybrid Visual-to-Code System

### Flow Compilation Process
```
Visual Editor → JSON Definition → Python AST → Executable Code
```

### Example Transformation
**Visual Flow JSON:**
```json
{
  "nodes": [
    {"id": "input_1", "type": "TextInput", "config": {"placeholder": "Enter text"}},
    {"id": "llm_1", "type": "OpenAI", "config": {"model": "gpt-4"}}
  ],
  "connections": [{"source": "input_1", "target": "llm_1"}]
}
```

**Generated Python Code:**
```python
async def execute_flow(inputs):
    input_1 = TextInputNode(placeholder="Enter text")
    llm_1 = OpenAINode(model="gpt-4")
    
    result_1 = await input_1.process(inputs)
    result_2 = await llm_1.process(result_1)
    
    return result_2
```

## 🗄️ Database Schema

### Core Tables
```sql
-- User Management
users (id, name, email, password_hash, role, status, created_at, updated_at)
projects (id, name, description, owner_id, status, settings, created_at, updated_at)
user_projects (user_id, project_id, role, joined_at)

-- Flow System
flows (id, project_id, name, description, definition, status, version, created_by, created_at, updated_at)
flow_versions (id, flow_id, version, definition, changes_summary, created_by, created_at)

-- Execution System
executions (id, flow_id, user_id, status, inputs, outputs, start_time, end_time, execution_time_ms, node_results)
execution_logs (id, execution_id, node_id, level, message, metadata, timestamp)

-- Node System
custom_nodes (id, name, description, code, metadata, created_by, status, created_at, updated_at)

-- Audit System
audit_logs (id, user_id, action, resource_type, resource_id, old_values, new_values, ip_address, user_agent, created_at)
```

### Key Relationships
- Users can own multiple Projects
- Projects contain multiple Flows
- Flows have multiple Executions
- Users can be assigned to Projects with specific roles

## 🔌 Node System Architecture

### Base Node Structure
```python
class BaseNode(ABC):
    @property
    @abstractmethod
    def metadata(self) -> NodeMetadata:
        pass
    
    @property
    @abstractmethod
    def input_ports(self) -> List[NodePort]:
        pass
    
    @property
    @abstractmethod
    def output_ports(self) -> List[NodePort]:
        pass
    
    @abstractmethod
    async def _execute_logic(self, context: ExecutionContext) -> Dict[str, Any]:
        pass
```

### Node Registry System
- Dynamic node discovery and registration
- Plugin-based architecture for custom nodes
- Type validation and parameter schemas
- Automatic documentation generation

## 🚀 Execution Engine

### Async Execution Pipeline
1. **Flow Validation**: Check node compatibility and connections
2. **Dependency Resolution**: Topological sorting for execution order
3. **Parallel Execution**: Run independent nodes concurrently
4. **Result Aggregation**: Collect and format execution results
5. **Error Handling**: Graceful failure management

### Execution Context
```python
@dataclass
class ExecutionContext:
    execution_id: str
    node_id: str
    inputs: Dict[str, Any]
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]
    user_id: Optional[str] = None
```

## 🔐 Security Architecture

### Authentication & Authorization
- **JWT Tokens**: Stateless authentication
- **Role-Based Access Control**: Hierarchical permissions
- **Resource-Level Security**: Fine-grained access control
- **Audit Logging**: Complete action tracking

### API Security
- **Input Validation**: Pydantic schemas for all endpoints
- **Rate Limiting**: Prevent abuse and DoS attacks
- **CORS Configuration**: Secure cross-origin requests
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📊 Performance Optimizations

### Database Performance
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Indexed queries and eager loading
- **Caching Strategy**: Redis for frequently accessed data
- **Async Operations**: Non-blocking database operations

### Execution Performance
- **Parallel Processing**: Concurrent node execution
- **Compilation Caching**: Cache compiled flows
- **Resource Management**: Memory and CPU optimization
- **Load Balancing**: Distribute execution load

## 🔄 Real-time Features

### WebSocket Architecture
- **Socket.io Integration**: Real-time bidirectional communication
- **Room Management**: Flow-specific communication channels
- **Event Broadcasting**: Live updates to connected clients
- **Connection Management**: Robust reconnection handling

### Real-time Capabilities
- **Live Flow Editing**: Multi-user collaborative editing
- **Execution Monitoring**: Real-time execution progress
- **User Presence**: Show active users and cursors
- **Instant Notifications**: System alerts and updates

## 🧪 Testing Strategy

### Backend Testing
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **End-to-End Tests**: Complete workflow testing
- **Performance Tests**: Load and stress testing

### Frontend Testing
- **Component Tests**: React component testing
- **Canvas Tests**: Visual editor functionality
- **API Integration Tests**: Frontend-backend communication
- **User Journey Tests**: Complete user workflows

## 📦 Deployment Architecture

### Development Environment
- **Docker Compose**: Local development setup
- **Hot Reloading**: Fast development cycles
- **Debug Tools**: Comprehensive debugging support
- **Test Data**: Automated seeding and fixtures

### Production Environment
- **Containerization**: Docker-based deployment
- **Orchestration**: Kubernetes support
- **Monitoring**: Health checks and metrics
- **Scaling**: Horizontal and vertical scaling

## 🔧 Configuration Management

### Environment Configuration
- **Environment Variables**: Secure configuration management
- **Config Classes**: Structured configuration objects
- **Validation**: Configuration validation at startup
- **Secrets Management**: Secure handling of sensitive data

### Feature Flags
- **Dynamic Configuration**: Runtime feature toggling
- **A/B Testing**: Gradual feature rollouts
- **Environment-Specific**: Different configs per environment
- **User-Based**: Per-user feature access

## 📈 Monitoring & Observability

### Application Monitoring
- **Health Checks**: Service availability monitoring
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Exception monitoring and alerting
- **Resource Usage**: CPU, memory, and disk monitoring

### Business Metrics
- **User Analytics**: Usage patterns and adoption
- **Flow Metrics**: Execution statistics and performance
- **System Metrics**: Overall platform health
- **Custom Metrics**: Domain-specific measurements

This architecture provides a solid foundation for building a scalable, maintainable, and high-performance visual flow builder that can handle enterprise-scale workloads while maintaining developer productivity and user experience.