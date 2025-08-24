# Flower - Visual Flow Builder Project Documentation

## Project Vision

Flower is a next-generation visual flow builder designed to address Langflow's architectural limitations through modern software engineering practices. Built with FastAPI and Porto architecture, it provides a scalable, maintainable, and high-performance alternative for AI workflow orchestration.

## Core Improvements Over Langflow

### 1. **Architecture Foundation**
- **Porto Pattern**: Modular container-based architecture for scalability
- **Async/Await**: Full asynchronous processing throughout the system
- **Type Safety**: Complete Pydantic validation and SQLAlchemy models
- **Dependency Injection**: Loose coupling and testable components

### 2. **Performance Enhancements**
- Optimized execution engine with async processing
- Efficient database operations with SQLAlchemy
- Redis caching for improved response times
- WebSocket support for real-time updates

### 3. **Developer Experience**
- Clear separation of concerns
- Built-in testing framework
- Plugin-based node system
- Comprehensive error handling

## Architecture Overview

### Porto Architecture Implementation

```
app/
├── Ship/                    # Framework layer
│   ├── Engine/             # Core application engine
│   ├── Features/           # Cross-cutting features
│   ├── Parents/            # Base classes
│   └── Middlewares/        # HTTP middlewares
├── Containers/             # Business modules
│   ├── Flow/               # Flow management
│   ├── Node/               # Node definitions
│   ├── Execution/          # Flow execution
│   ├── User/               # Authentication
│   └── Project/            # Workspace management
```

### Container Structure

Each container follows Porto conventions:

```
Container/
├── Actions/               # Business operations orchestration
├── Tasks/                # Specific business logic
├── Models/               # Business entities
├── Data/
│   ├── Repositories/     # Data access layer
│   ├── Migrations/       # Database migrations
│   └── Seeders/          # Test data
├── UI/
│   ├── API/
│   │   ├── Controllers/  # HTTP request handlers
│   │   ├── Requests/     # Input validation
│   │   ├── Transformers/ # Response formatting
│   │   └── Routes/       # API endpoints
│   └── WebSocket/        # Real-time communication
├── Tests/
│   ├── Unit/             # Component tests
│   └── Functional/       # Integration tests
└── Configs/              # Container configuration
```

## Core Containers

### 1. Flow Container
**Purpose**: Manages flow definitions, metadata, and lifecycle

**Key Components**:
- `CreateFlowAction`: Orchestrates flow creation
- `ExecuteFlowAction`: Handles flow execution
- `FlowRepository`: Data persistence
- `FlowModel`: Flow entity definition

### 2. Node Container
**Purpose**: Handles node types, configurations, and registry

**Key Components**:
- `RegisterNodeAction`: Node type registration
- `NodeFactory`: Dynamic node creation
- `NodeRepository`: Node configuration storage
- `BaseNode`: Abstract node implementation

### 3. Execution Container
**Purpose**: Tracks flow runs, results, and performance metrics

**Key Components**:
- `StartExecutionAction`: Initiates flow execution
- `ExecutionEngine`: Core execution logic
- `ExecutionRepository`: Run history storage
- `ExecutionModel`: Execution state tracking

### 4. User Container
**Purpose**: Authentication, authorization, and user management

**Key Components**:
- `AuthenticateUserAction`: User login
- `UserRepository`: User data management
- `UserModel`: User entity
- `JWTMiddleware`: Token validation

### 5. Project Container
**Purpose**: Workspace organization and collaboration

**Key Components**:
- `CreateProjectAction`: Project setup
- `ProjectRepository`: Project data
- `ProjectModel`: Project entity
- `CollaborationService`: Team features

## Technical Stack

### Backend
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: ORM with async support
- **Pydantic**: Data validation and serialization
- **Redis**: Caching and session storage
- **PostgreSQL**: Primary database
- **RabbitMQ**: Message broker for async processing

### Frontend (Future)
- **React/Vue.js**: Modern UI framework
- **WebSocket**: Real-time updates
- **Canvas API**: Visual flow editor
- **TypeScript**: Type-safe frontend development

## Key Features

### 1. **Visual Flow Editor**
- Drag-and-drop interface
- Real-time collaboration
- Version control integration
- Template library

### 2. **Execution Engine**
- Async node processing
- Parallel execution paths
- Error handling and recovery
- Performance monitoring

### 3. **Node System**
- Plugin-based architecture
- Custom node development
- Type validation
- Documentation generation

### 4. **Integration Capabilities**
- REST API endpoints
- WebSocket connections
- Message queue integration
- External service connectors

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure setup
- [x] Porto architecture implementation
- [ ] Database configuration
- [ ] Basic API endpoints
- [ ] Authentication system

### Phase 2: Core Features
- [ ] Flow management CRUD
- [ ] Node registry system
- [ ] Basic execution engine
- [ ] WebSocket integration
- [ ] Testing framework

### Phase 3: Advanced Features
- [ ] Visual editor interface
- [ ] Real-time collaboration
- [ ] Plugin system
- [ ] Performance monitoring
- [ ] Documentation system

### Phase 4: Production Ready
- [ ] Security hardening
- [ ] Performance optimization
- [ ] Deployment automation
- [ ] Monitoring and logging
- [ ] User documentation

## Lessons from Langflow Analysis

### Architectural Insights
Based on the Oganesson/Langflow analysis, key improvements include:

1. **Better Component Architecture**: Replace monolithic components with modular, testable units
2. **Enhanced Error Handling**: Implement comprehensive error handling at all levels
3. **Improved Integration**: Native support for message brokers and external systems
4. **Scalable Deployment**: Container-based architecture with proper service separation

### Technical Improvements
- **Null Safety**: Prevent runtime errors with proper validation
- **Template Processing**: Robust handling of dynamic content
- **Connection Management**: Reliable external service integration
- **Health Monitoring**: Built-in health checks and monitoring

## Best Practices

### Code Organization
- Follow Porto naming conventions
- Maintain clear separation of concerns
- Use dependency injection throughout
- Implement comprehensive testing

### Performance
- Async/await for all I/O operations
- Database query optimization
- Caching strategies
- Connection pooling

### Security
- Input validation at all entry points
- Authentication and authorization
- Secure configuration management
- Regular security audits

### Testing
- Unit tests for all business logic
- Integration tests for API endpoints
- End-to-end tests for critical workflows
- Performance testing for scalability

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Docker (optional)

### Installation
```bash
# Clone repository
git clone <repository-url>
cd flower

# Install dependencies
pip install -r requirements.txt

# Setup database
alembic upgrade head

# Run development server
uvicorn app.main:app --reload
```

### Development Workflow
1. Create feature branch
2. Implement changes following Porto patterns
3. Write comprehensive tests
4. Submit pull request
5. Code review and merge

## Contributing

### Guidelines
- Follow Porto architecture principles
- Maintain test coverage above 90%
- Document all public APIs
- Use type hints throughout
- Follow PEP 8 style guide

### Code Review Process
- Automated testing must pass
- Manual code review required
- Architecture compliance check
- Performance impact assessment

## Conclusion

Flower represents a modern approach to visual flow building, addressing the limitations of existing solutions through thoughtful architecture and engineering practices. By leveraging Porto architecture, FastAPI, and modern Python practices, it provides a solid foundation for scalable AI workflow orchestration.

The project's modular design ensures maintainability, while its async-first approach guarantees performance. With comprehensive testing and clear separation of concerns, Flower is positioned to become a reliable platform for complex workflow automation needs.