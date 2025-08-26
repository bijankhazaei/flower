# API Specifications - Complete Endpoint Documentation

## 🔐 Authentication

All API endpoints (except login) require JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

## 👥 User Management APIs

### Create User
```http
POST /api/users
Authorization: Bearer <token> (ADMIN+ required)
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com", 
  "password": "securepassword",
  "role": "USER"
}

Response 201:
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "USER",
  "status": "PENDING",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### List Users
```http
GET /api/users?page=1&limit=20&role=USER&status=ACTIVE
Authorization: Bearer <token> (ADMIN+ required)

Response 200:
{
  "users": [
    {
      "id": "uuid",
      "name": "John Doe", 
      "email": "john@example.com",
      "role": "USER",
      "status": "ACTIVE",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

### Get User Details
```http
GET /api/users/{user_id}
Authorization: Bearer <token>

Response 200:
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com", 
  "role": "USER",
  "status": "ACTIVE",
  "projects": [
    {
      "id": "uuid",
      "name": "My Project",
      "role": "EDITOR"
    }
  ],
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Update User
```http
PUT /api/users/{user_id}
Authorization: Bearer <token> (ADMIN+ or self)
Content-Type: application/json

{
  "name": "John Smith",
  "email": "johnsmith@example.com"
}

Response 200:
{
  "id": "uuid",
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "role": "USER", 
  "status": "ACTIVE",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Activate/Deactivate User
```http
POST /api/users/{user_id}/activate
POST /api/users/{user_id}/deactivate
Authorization: Bearer <token> (ADMIN+ required)

Response 200:
{
  "id": "uuid",
  "status": "ACTIVE", // or "INACTIVE"
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Change User Role
```http
PUT /api/users/{user_id}/role
Authorization: Bearer <token> (SUPER_ADMIN required)
Content-Type: application/json

{
  "role": "ADMIN"
}

Response 200:
{
  "id": "uuid",
  "role": "ADMIN",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## 📁 Project Management APIs

### Create Project
```http
POST /api/projects
Authorization: Bearer <token> (ADMIN+ required)
Content-Type: application/json

{
  "name": "AI Workflow Project",
  "description": "Project for AI workflow automation",
  "settings": {
    "auto_save": true,
    "collaboration": true
  }
}

Response 201:
{
  "id": "uuid",
  "name": "AI Workflow Project",
  "description": "Project for AI workflow automation",
  "owner_id": "uuid",
  "status": "ACTIVE",
  "settings": {
    "auto_save": true,
    "collaboration": true
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

### List User Projects
```http
GET /api/projects?status=ACTIVE&role=EDITOR
Authorization: Bearer <token>

Response 200:
{
  "projects": [
    {
      "id": "uuid",
      "name": "AI Workflow Project",
      "description": "Project description",
      "owner_id": "uuid",
      "status": "ACTIVE",
      "user_role": "EDITOR",
      "flow_count": 5,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### Get Project Details
```http
GET /api/projects/{project_id}
Authorization: Bearer <token>

Response 200:
{
  "id": "uuid",
  "name": "AI Workflow Project",
  "description": "Project description",
  "owner": {
    "id": "uuid",
    "name": "Owner Name",
    "email": "owner@example.com"
  },
  "status": "ACTIVE",
  "settings": {},
  "users": [
    {
      "id": "uuid",
      "name": "User Name",
      "role": "EDITOR",
      "joined_at": "2024-01-01T00:00:00Z"
    }
  ],
  "flows": [
    {
      "id": "uuid", 
      "name": "Flow Name",
      "status": "ACTIVE",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Add User to Project
```http
POST /api/projects/{project_id}/users
Authorization: Bearer <token> (ADMIN+ required)
Content-Type: application/json

{
  "user_id": "uuid",
  "role": "EDITOR"
}

Response 200:
{
  "user_id": "uuid",
  "project_id": "uuid", 
  "role": "EDITOR",
  "joined_at": "2024-01-01T00:00:00Z"
}
```

## 🌊 Flow Management APIs

### Create Flow
```http
POST /api/projects/{project_id}/flows
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Text Processing Flow",
  "description": "Flow for processing text data",
  "definition": {
    "nodes": [
      {
        "id": "input_1",
        "type": "InputNode",
        "position": {"x": 100, "y": 100},
        "parameters": {"input_key": "text"}
      }
    ],
    "connections": []
  }
}

Response 201:
{
  "id": "uuid",
  "project_id": "uuid",
  "name": "Text Processing Flow",
  "description": "Flow description",
  "definition": {...},
  "status": "DRAFT",
  "version": 1,
  "created_by": "uuid",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### List Project Flows
```http
GET /api/projects/{project_id}/flows?status=ACTIVE&page=1&limit=20
Authorization: Bearer <token>

Response 200:
{
  "flows": [
    {
      "id": "uuid",
      "name": "Text Processing Flow",
      "description": "Flow description", 
      "status": "ACTIVE",
      "version": 1,
      "node_count": 5,
      "execution_count": 10,
      "last_executed": "2024-01-01T00:00:00Z",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

### Get Flow Details
```http
GET /api/flows/{flow_id}
Authorization: Bearer <token>

Response 200:
{
  "id": "uuid",
  "project_id": "uuid",
  "name": "Text Processing Flow",
  "description": "Flow description",
  "definition": {
    "nodes": [...],
    "connections": [...]
  },
  "status": "ACTIVE",
  "version": 1,
  "created_by": {
    "id": "uuid",
    "name": "Creator Name"
  },
  "executions": [
    {
      "id": "uuid",
      "status": "COMPLETED",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Execute Flow
```http
POST /api/flows/{flow_id}/execute
Authorization: Bearer <token>
Content-Type: application/json

{
  "inputs": {
    "text": "Hello World"
  },
  "parameters": {
    "timeout": 300
  }
}

Response 200:
{
  "execution_id": "uuid",
  "status": "RUNNING",
  "start_time": "2024-01-01T00:00:00Z"
}
```

## ⚙️ Node Management APIs

### List Node Types
```http
GET /api/nodes/types?category=Input/Output
Authorization: Bearer <token>

Response 200:
{
  "node_types": [
    {
      "name": "InputNode",
      "metadata": {
        "name": "Input Node",
        "description": "Accepts input data",
        "category": "Input/Output"
      },
      "input_ports": [],
      "output_ports": [
        {
          "name": "output",
          "data_type": "text",
          "required": true
        }
      ],
      "parameters_schema": [
        {
          "name": "input_key", 
          "data_type": "text",
          "required": true,
          "description": "Key for input data"
        }
      ]
    }
  ],
  "count": 1
}
```

### Get Node Type Details
```http
GET /api/nodes/types/{node_type}
Authorization: Bearer <token>

Response 200:
{
  "name": "TextProcessorNode",
  "metadata": {
    "name": "Text Processor",
    "description": "Processes text data",
    "category": "Processing"
  },
  "input_ports": [
    {
      "name": "text",
      "data_type": "text", 
      "required": true
    }
  ],
  "output_ports": [
    {
      "name": "processed_text",
      "data_type": "text",
      "required": true
    }
  ],
  "parameters_schema": [
    {
      "name": "operation",
      "data_type": "text",
      "required": true,
      "options": ["uppercase", "lowercase", "capitalize"]
    }
  ]
}
```

## 📊 Execution Management APIs

### List Executions
```http
GET /api/executions?status=COMPLETED&limit=50&flow_id=uuid
Authorization: Bearer <token>

Response 200:
{
  "executions": [
    {
      "id": "uuid",
      "flow_id": "uuid",
      "flow_name": "Text Processing Flow",
      "status": "COMPLETED",
      "start_time": "2024-01-01T00:00:00Z",
      "end_time": "2024-01-01T00:00:05Z",
      "execution_time_ms": 5000,
      "user": {
        "id": "uuid",
        "name": "User Name"
      }
    }
  ],
  "total": 1,
  "count": 1
}
```

### Get Execution Details
```http
GET /api/executions/{execution_id}
Authorization: Bearer <token>

Response 200:
{
  "id": "uuid",
  "flow_id": "uuid",
  "user_id": "uuid",
  "status": "COMPLETED",
  "inputs": {
    "text": "Hello World"
  },
  "outputs": {
    "result": "HELLO WORLD"
  },
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-01T00:00:05Z",
  "execution_time_ms": 5000,
  "node_results": {
    "input_1": {
      "success": true,
      "outputs": {"output": "Hello World"},
      "execution_time": 100
    },
    "processor_1": {
      "success": true, 
      "outputs": {"processed_text": "HELLO WORLD"},
      "execution_time": 200
    }
  }
}
```

### Cancel Execution
```http
POST /api/executions/{execution_id}/cancel
Authorization: Bearer <token>

Response 200:
{
  "id": "uuid",
  "status": "CANCELLED",
  "end_time": "2024-01-01T00:00:00Z"
}
```

## 🚨 Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "reason": "Email already exists"
    }
  }
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (duplicate resource)
- `500` - Internal Server Error