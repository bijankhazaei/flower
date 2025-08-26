import { ApiActions, RawService } from '@/services/apiService';

export interface Flow {
  id: string;
  name: string;
  description?: string;
  definition: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface CreateFlowRequest {
  name: string;
  description?: string;
  definition?: Record<string, any>;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    role: string;
  };
}

export default ((api: RawService) => ({
  // Auth endpoints
  login: (credentials: LoginRequest) => 
    api.post<LoginResponse>('/auth/login', credentials),
  
  // Flow endpoints
  flowList: (page = 1) => 
    api.get<Flow[]>(`/flows?page=${page}`),
  
  createFlow: (flow: CreateFlowRequest) => 
    api.post<Flow>('/flows', flow),
  
  getFlow: (id: string) => 
    api.get<Flow>(`/flows/${id}`),
  
  updateFlow: (id: string, flow: Partial<CreateFlowRequest>) => 
    api.put<Flow>(`/flows/${id}`, flow),
  
  deleteFlow: (id: string) => 
    api.delete<void>(`/flows/${id}`),
  
  // Compiler endpoints
  compileFlow: (definition: Record<string, any>) => 
    api.post<{ code: string }>('/compiler/compile', { flow_definition: definition }),
  
  executeFlow: (definition: Record<string, any>, inputs: Record<string, any>) => 
    api.post<{ result: any }>('/compiler/execute', { flow_definition: definition, inputs }),
})) satisfies ApiActions;