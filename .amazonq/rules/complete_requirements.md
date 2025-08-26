# Flower Complete Requirements

## 🎯 Mission & Vision

**Mission**: Build a next-generation visual flow builder that addresses Langflow's architectural limitations through modern software engineering practices, providing a scalable, maintainable, and high-performance platform for AI workflow orchestration.

**Vision**: Create a comprehensive platform where users can visually design, manage, and execute complex AI workflows with enterprise-grade features including user management, project organization, and real-time collaboration.

## 🏗️ Core Entity Structure

### User Management Hierarchy
```
SUPER_ADMIN (System Level)
├── Can manage all users, projects, and system settings
├── Access to all projects and flows
└── System monitoring and configuration

ADMIN (Organization Level)  
├── Can manage users within their organization
├── Can create and manage projects
└── Can assign users to projects

USER (Project Level)
├── Can access assigned projects
├── Can create and edit flows within projects
└── Can execute flows they have access to
```

### Entity Relationships
```
User (1) ──── (N) UserProject ──── (N) Project
Project (1) ──── (N) Flow
Flow (1) ──── (N) Node
Flow (1) ──── (N) Connection
Flow (1) ──── (N) Execution
```

## 📋 Complete CRUD Requirements

### User Management APIs
```
POST   /api/users                    # Create user (ADMIN+)
GET    /api/users                    # List users (ADMIN+)
GET    /api/users/{id}               # Get user details
PUT    /api/users/{id}               # Update user (ADMIN+ or self)
DELETE /api/users/{id}               # Delete user (SUPER_ADMIN)
POST   /api/users/{id}/activate      # Activate user (ADMIN+)
POST   /api/users/{id}/deactivate    # Deactivate user (ADMIN+)
PUT    /api/users/{id}/role          # Change user role (SUPER_ADMIN)
```

### Project Management APIs
```
POST   /api/projects                 # Create project (ADMIN+)
GET    /api/projects                 # List user's projects
GET    /api/projects/{id}            # Get project details
PUT    /api/projects/{id}            # Update project (ADMIN+ or owner)
DELETE /api/projects/{id}            # Delete project (ADMIN+ or owner)
POST   /api/projects/{id}/users      # Add user to project (ADMIN+)
DELETE /api/projects/{id}/users/{uid} # Remove user from project (ADMIN+)
GET    /api/projects/{id}/users      # List project users
PUT    /api/projects/{id}/status     # Update project status
```

### Flow Management APIs
```
POST   /api/projects/{pid}/flows     # Create flow
GET    /api/projects/{pid}/flows     # List project flows
GET    /api/flows/{id}               # Get flow details
PUT    /api/flows/{id}               # Update flow
DELETE /api/flows/{id}               # Delete flow
POST   /api/flows/{id}/duplicate     # Duplicate flow
PUT    /api/flows/{id}/status        # Update flow status
GET    /api/flows/{id}/versions      # Get flow versions
POST   /api/flows/{id}/versions      # Create new version
```

### Node Management APIs
```
GET    /api/nodes/types              # List available node types
GET    /api/nodes/types/{type}       # Get node type details
POST   /api/nodes/validate           # Validate node configuration
POST   /api/nodes/custom             # Upload custom node (ADMIN+)
GET    /api/flows/{id}/nodes         # Get flow nodes
POST   /api/flows/{id}/nodes         # Add node to flow
PUT    /api/flows/{id}/nodes/{nid}   # Update node
DELETE /api/flows/{id}/nodes/{nid}   # Delete node
```

### Execution Management APIs
```
POST   /api/flows/{id}/execute       # Execute flow
GET    /api/executions               # List user executions
GET    /api/executions/{id}          # Get execution details
POST   /api/executions/{id}/cancel   # Cancel execution
GET    /api/executions/{id}/logs     # Get execution logs
POST   /api/executions/cleanup       # Cleanup old executions
```

## 🔄 Status Management System

### User Status
- `ACTIVE` - Can login and access assigned resources
- `INACTIVE` - Cannot login, account suspended
- `PENDING` - Awaiting activation by admin

### Project Status
- `ACTIVE` - Project is active and accessible
- `ARCHIVED` - Project is archived but accessible
- `SUSPENDED` - Project access is temporarily suspended
- `DELETED` - Soft deleted, recoverable by admin

### Flow Status
- `DRAFT` - Flow is being developed
- `ACTIVE` - Flow is ready for execution
- `TESTING` - Flow is in testing phase
- `DEPRECATED` - Flow is deprecated but still accessible
- `ARCHIVED` - Flow is archived

### Execution Status
- `PENDING` - Execution is queued
- `RUNNING` - Execution is in progress
- `COMPLETED` - Execution completed successfully
- `FAILED` - Execution failed with errors
- `CANCELLED` - Execution was cancelled by user
- `TIMEOUT` - Execution exceeded time limit

## 🔐 Permission Matrix

| Action | USER | ADMIN | SUPER_ADMIN |
|--------|------|-------|-------------|
| Create User | ❌ | ✅ | ✅ |
| Manage Users | ❌ | ✅ (org) | ✅ (all) |
| Create Project | ❌ | ✅ | ✅ |
| Manage Projects | ✅ (assigned) | ✅ (owned) | ✅ (all) |
| Create Flow | ✅ | ✅ | ✅ |
| Execute Flow | ✅ | ✅ | ✅ |
| Upload Custom Nodes | ❌ | ✅ | ✅ |
| System Settings | ❌ | ❌ | ✅ |

## 📊 Additional Features Required

### Analytics & Monitoring
- Execution statistics per user/project/flow
- Performance metrics and bottlenecks
- Resource usage tracking
- Error rate monitoring

### Collaboration Features
- Real-time flow editing (WebSocket)
- Comment system on flows
- Change history and version control
- Flow sharing and templates

### Enterprise Features
- Audit logging for all actions
- Backup and restore functionality
- API rate limiting
- SSO integration support

## ✅ Implementation Status

### Completed
- [x] Basic User model with roles (USER, ADMIN, SUPER_ADMIN)
- [x] Authentication system with JWT
- [x] Flow compilation and execution engine
- [x] Node system with registry
- [x] Basic API endpoints for compiler and nodes
- [x] Docker setup with all services

### In Progress
- [ ] Complete CRUD for all entities
- [ ] Project management system
- [ ] User-Project associations
- [ ] Status management implementation
- [ ] Permission system enforcement

### Pending
- [ ] Frontend visual editor
- [ ] Real-time collaboration
- [ ] Analytics and monitoring
- [ ] Enterprise features