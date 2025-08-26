// Flow API Types
export interface Flow {
  id: string;
  name: string;
  description?: string;
  nodes: FlowNode[];
  connections: Connection[];
  created_at: string;
  updated_at: string;
}

export interface CreateFlowRequest {
  name: string;
  description?: string;
}

export interface UpdateFlowRequest {
  name?: string;
  description?: string;
  nodes?: FlowNode[];
  connections?: Connection[];
}

// Node API Types
export interface NodeType {
  id: string;
  name: string;
  category: string;
  description: string;
  input_ports: Port[];
  output_ports: Port[];
  config_schema: Record<string, any>;
}

export interface Port {
  name: string;
  data_type: string;
  required: boolean;
}

// Execution API Types
export interface ExecutionRequest {
  flow_id: string;
  inputs?: Record<string, any>;
}

export interface ExecutionResponse {
  execution_id: string;
  status: 'running' | 'completed' | 'failed';
  results?: Record<string, any>;
  error?: string;
}

export interface ExecutionStatus {
  id: string;
  flow_id: string;
  status: 'running' | 'completed' | 'failed';
  started_at: string;
  completed_at?: string;
  results?: Record<string, any>;
  error?: string;
}

// User API Types
export interface User {
  id: string;
  email: string;
  role: 'USER' | 'ADMIN' | 'SUPER_ADMIN';
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  user: User;
}

// Common API Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  error: string;
  details?: Record<string, any>;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
}

// Re-export component types
export type { FlowNode, Connection } from '@/contracts/components';