# Database Schema - Complete Design

## 🗄️ Complete Database Schema

### Users Table
```sql
users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('USER', 'ADMIN', 'SUPER_ADMIN') DEFAULT 'USER',
  status ENUM('ACTIVE', 'INACTIVE', 'PENDING') DEFAULT 'PENDING',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

### Projects Table
```sql
projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
  status ENUM('ACTIVE', 'ARCHIVED', 'SUSPENDED', 'DELETED') DEFAULT 'ACTIVE',
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

### User-Project Association
```sql
user_projects (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  role ENUM('OWNER', 'EDITOR', 'VIEWER') DEFAULT 'VIEWER',
  joined_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (user_id, project_id)
)
```

### Flows Table
```sql
flows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  definition JSONB NOT NULL,
  status ENUM('DRAFT', 'ACTIVE', 'TESTING', 'DEPRECATED', 'ARCHIVED') DEFAULT 'DRAFT',
  version INTEGER DEFAULT 1,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

### Flow Versions Table
```sql
flow_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  flow_id UUID REFERENCES flows(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,
  definition JSONB NOT NULL,
  changes_summary TEXT,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(flow_id, version)
)
```

### Executions Table
```sql
executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  flow_id UUID REFERENCES flows(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  status ENUM('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT') DEFAULT 'PENDING',
  inputs JSONB,
  outputs JSONB,
  error_message TEXT,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  execution_time_ms INTEGER,
  node_results JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
)
```

### Execution Logs Table
```sql
execution_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  execution_id UUID REFERENCES executions(id) ON DELETE CASCADE,
  node_id VARCHAR(255),
  level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR') DEFAULT 'INFO',
  message TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  timestamp TIMESTAMP DEFAULT NOW()
)
```

### Custom Nodes Table
```sql
custom_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL UNIQUE,
  description TEXT,
  code TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  status ENUM('ACTIVE', 'DEPRECATED', 'DISABLED') DEFAULT 'ACTIVE',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

### Audit Logs Table
```sql
audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  action VARCHAR(255) NOT NULL,
  resource_type VARCHAR(100) NOT NULL,
  resource_id UUID,
  old_values JSONB,
  new_values JSONB,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT NOW()
)
```

## 📊 Indexes for Performance

```sql
-- User indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);

-- Project indexes
CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);

-- User-Project indexes
CREATE INDEX idx_user_projects_user ON user_projects(user_id);
CREATE INDEX idx_user_projects_project ON user_projects(project_id);

-- Flow indexes
CREATE INDEX idx_flows_project ON flows(project_id);
CREATE INDEX idx_flows_created_by ON flows(created_by);
CREATE INDEX idx_flows_status ON flows(status);

-- Execution indexes
CREATE INDEX idx_executions_flow ON executions(flow_id);
CREATE INDEX idx_executions_user ON executions(user_id);
CREATE INDEX idx_executions_status ON executions(status);
CREATE INDEX idx_executions_created_at ON executions(created_at);

-- Execution logs indexes
CREATE INDEX idx_execution_logs_execution ON execution_logs(execution_id);
CREATE INDEX idx_execution_logs_timestamp ON execution_logs(timestamp);

-- Audit logs indexes
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

## 🔄 Migration Strategy

### Phase 1: Core Entities
1. Users table (already exists)
2. Projects table
3. User-Project association table

### Phase 2: Flow System
1. Flows table (enhance existing)
2. Flow versions table
3. Update executions table

### Phase 3: Advanced Features
1. Custom nodes table
2. Execution logs table
3. Audit logs table

## 📝 Model Relationships

### SQLAlchemy Relationships
```python
# User Model
class User(BaseModel):
    projects = relationship("UserProject", back_populates="user")
    owned_projects = relationship("Project", back_populates="owner")
    executions = relationship("Execution", back_populates="user")

# Project Model  
class Project(BaseModel):
    owner = relationship("User", back_populates="owned_projects")
    users = relationship("UserProject", back_populates="project")
    flows = relationship("Flow", back_populates="project")

# Flow Model
class Flow(BaseModel):
    project = relationship("Project", back_populates="flows")
    created_by_user = relationship("User")
    executions = relationship("Execution", back_populates="flow")
    versions = relationship("FlowVersion", back_populates="flow")

# Execution Model
class Execution(BaseModel):
    flow = relationship("Flow", back_populates="executions")
    user = relationship("User", back_populates="executions")
    logs = relationship("ExecutionLog", back_populates="execution")
```