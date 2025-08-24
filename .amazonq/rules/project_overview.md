# Flower - Visual Flow Builder

## Project Overview

Flower is a visual flow builder built with FastAPI and Porto architecture, designed to address Langflow's weaknesses:

### Key Improvements over Langflow

1. **Better Architecture**: Porto pattern for scalability and maintainability
2. **Performance**: Async/await throughout, optimized execution engine
3. **Type Safety**: Full Pydantic validation and SQLAlchemy models
4. **Modularity**: Clear separation of concerns with containers
5. **Testing**: Built-in test structure for reliability
6. **Extensibility**: Plugin-based node system

### Core Containers

- **Flow**: Manages flow definitions and metadata
- **Node**: Handles node types and configurations  
- **Execution**: Tracks flow runs and results
- **User**: Authentication and user management
- **Project**: Workspace organization

### Architecture Benefits

- **Scalable**: Each container can be developed independently
- **Testable**: Clear interfaces for unit/integration testing
- **Maintainable**: Consistent structure across all modules
- **Extensible**: Easy to add new node types and features

### Next Steps

1. Implement dependency injection
2. Add database configuration
3. Create execution engine
4. Build node registry system
5. Add WebSocket support for real-time updates