# Flower Frontend Implementation Guide (Zeenome-Inspired)

## Phase 1: Project Setup with Improved Architecture

### 1. Project Initialization
```bash
# Create React app with TypeScript
npx create-react-app flower-frontend --template typescript
cd flower-frontend

# Core dependencies
npm install zustand jotai react-query axios
npm install @radix-ui/react-slot @radix-ui/react-dialog @radix-ui/react-select
npm install tailwindcss @tailwindcss/forms class-variance-authority clsx
npm install react-hook-form @hookform/resolvers zod
npm install framer-motion lucide-react

# Development dependencies
npm install -D @types/node eslint-config-prettier prettier
```

### 2. Directory Structure Setup
```bash
mkdir -p src/{components/{kit,layouts,ui},contracts/{app,base,components,ui},services/{apiService},store,modules/{auth,resolver,canvas},utilities,configs,stylesheets}

# Kit components structure
mkdir -p src/components/kit/{Button,Input,Card,Modal,Canvas,Node,Connection}

# UI components structure  
mkdir -p src/components/ui/{FlowCanvas,NodePalette,PropertyPanel,Toolbar}

# Services structure
mkdir -p src/services/{apiService,canvasService,flowService,nodeService}
```

### 3. Core Configuration Files

#### Tailwind Config with Design System
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Design system colors (inspired by Zeenome)
        gray: {
          50: '#f9fafb',
          100: '#f3f4f6',
          // ... full gray scale
          900: '#111827',
          950: '#030712'
        },
        dominant: {
          100: '#dbeafe',
          200: '#bfdbfe',
          // ... brand colors
          800: '#1e40af',
          900: '#1e3a8a'
        },
        complement: {
          100: '#dcfce7',
          // ... success colors
          900: '#14532d'
        },
        error: {
          100: '#fee2e2',
          // ... error colors
          900: '#7f1d1d'
        }
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem'
      }
    }
  },
  plugins: [require('@tailwindcss/forms')]
};
```

#### App Configuration
```typescript
// src/configs/app.config.ts
export const AppConfig = {
  api: {
    baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
    timeout: 10000,
  },
  canvas: {
    defaultZoom: 1,
    minZoom: 0.1,
    maxZoom: 3,
    gridSize: 20,
  },
  ui: {
    sidebarWidth: 320,
    toolbarHeight: 64,
    propertyPanelWidth: 280,
  }
};

// src/configs/index.ts
export { AppConfig } from './app.config';
```

## Phase 2: Kit Component System

### 1. Component Contracts
```typescript
// src/contracts/components/index.ts
import { ReactNode, HTMLAttributes } from 'react';

export interface ButtonProps extends HTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: ReactNode;
}

export interface CanvasProps extends HTMLAttributes<HTMLDivElement> {
  zoom: number;
  pan: { x: number; y: number };
  mode: 'select' | 'connect' | 'pan' | 'add-node';
  onCanvasClick?: (event: MouseEvent) => void;
  children?: ReactNode;
}

export interface NodeProps {
  node: FlowNode;
  isSelected: boolean;
  onDrag?: (offset: { x: number; y: number }) => void;
  onClick?: (nodeId: string) => void;
  onPortClick?: (port: Port) => void;
}

export interface KitComponents {
  Button: React.FC<ButtonProps>;
  Canvas: React.FC<CanvasProps>;
  Node: React.FC<NodeProps>;
  Connection: React.FC<ConnectionProps>;
  Card: React.FC<CardProps>;
  Modal: React.FC<ModalProps>;
  Input: React.FC<InputProps>;
  Select: React.FC<SelectProps>;
}
```

### 2. Kit Components Implementation
```typescript
// src/components/kit/Button/Button.tsx
import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/utilities/helpers';
import { ButtonProps } from '@/contracts/components';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-dominant-600 text-white hover:bg-dominant-700',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        ghost: 'hover:bg-gray-100 hover:text-gray-900',
        destructive: 'bg-error-600 text-white hover:bg-error-700'
      },
      size: {
        sm: 'h-8 px-3 text-xs',
        md: 'h-10 px-4 py-2',
        lg: 'h-12 px-8 text-base'
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md'
    }
  }
);

export const Button: React.FC<ButtonProps> = ({
  className,
  variant,
  size,
  children,
  ...props
}) => {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    >
      {children}
    </button>
  );
};
```

```typescript
// src/components/kit/Canvas/Canvas.tsx
import React, { forwardRef } from 'react';
import { cn } from '@/utilities/helpers';
import { CanvasProps } from '@/contracts/components';

export const Canvas = forwardRef<HTMLDivElement, CanvasProps>(({
  zoom,
  pan,
  mode,
  onCanvasClick,
  children,
  className,
  ...props
}, ref) => {
  return (
    <div
      ref={ref}
      className={cn('relative w-full h-full overflow-hidden', className)}
      onClick={onCanvasClick}
      {...props}
    >
      {/* Grid background */}
      <div className="absolute inset-0 opacity-20">
        <svg width="100%" height="100%">
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e5e7eb" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>
      
      {/* Canvas content */}
      <div
        className="absolute inset-0"
        style={{
          transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
          transformOrigin: '0 0'
        }}
      >
        {children}
      </div>
    </div>
  );
});

Canvas.displayName = 'Canvas';
```

### 3. Resolver System
```typescript
// src/modules/resolver/Resolver.tsx
import { Button } from '@/components/kit/Button/Button';
import { Canvas } from '@/components/kit/Canvas/Canvas';
import { Node } from '@/components/kit/Node/Node';
import { Connection } from '@/components/kit/Connection/Connection';
import { Card } from '@/components/kit/Card/Card';
import { Modal } from '@/components/kit/Modal/Modal';
import { Input } from '@/components/kit/Input/Input';
import { Select } from '@/components/kit/Select/Select';

export const Resolver = {
  Button,
  Canvas,
  Node,
  Connection,
  Card,
  Modal,
  Input,
  Select,
} as const;

// Type-safe resolver
export type ResolverComponents = typeof Resolver;
```

## Phase 3: API Service Layer

### 1. API Actions (Auto-generated Pattern)
```typescript
// src/app/flows/actions.tsx (or src/services/apiService/flows.actions.ts)
import { ApiActions } from '@/contracts/app/apiActions';

export default (
  (api: ApiType.RawService) => ({
    // Flow CRUD
    flowList: (page = 1, limit = 10) =>
      api.get<PaginatedResponse<Flow>>(`/flows?page=${page}&limit=${limit}`),
    
    flowById: (id: string) =>
      api.get<Flow>(`/flows/${id}`),
    
    createFlow: (flow: CreateFlowRequest) =>
      api.post<Flow>('/flows', flow),
    
    updateFlow: (id: string, updates: UpdateFlowRequest) =>
      api.put<Flow>(`/flows/${id}`, updates),
    
    deleteFlow: (id: string) =>
      api.delete<void>(`/flows/${id}`),
    
    // Compilation
    compileFlow: (flowDefinition: FlowDefinition) =>
      api.post<CompilationResult>('/compiler/compile', { flow_definition: flowDefinition }),
    
    executeFlow: (flowDefinition: FlowDefinition, inputs: any) =>
      api.post<ExecutionResult>('/compiler/execute', { 
        flow_definition: flowDefinition, 
        inputs 
      }),
    
    // Templates
    templateList: (category?: string) =>
      api.get<Template[]>(`/templates${category ? `?category=${category}` : ''}`),
    
    createTemplate: (template: CreateTemplateRequest) =>
      api.post<Template>('/templates', template),
  })
) satisfies ApiActions;

// Type definitions
export interface Flow {
  id: string;
  name: string;
  description?: string;
  nodes: FlowNode[];
  connections: Connection[];
  created_at: string;
  updated_at: string;
}

export interface FlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  config: Record<string, any>;
}

export interface Connection {
  id: string;
  source: string;
  target: string;
  sourcePort?: string;
  targetPort?: string;
}

export interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  flow_definition: FlowDefinition;
  is_public: boolean;
}
```

### 2. API Service Implementation
```typescript
// src/services/apiService/useApi.ts
import { useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { createApiService } from './instantiateAxios';

export const useApi = () => {
  const queryClient = useQueryClient();
  
  const api = useMemo(() => createApiService({
    baseURL: AppConfig.api.baseUrl,
    timeout: AppConfig.api.timeout,
    // Add auth token from localStorage
    headers: {
      Authorization: `Bearer ${localStorage.getItem('auth_token') || ''}`
    }
  }), []);
  
  return api;
};

// React Query hooks for common operations
export const useFlows = (page = 1, limit = 10) => {
  const api = useApi();
  return useQuery(['flows', page, limit], () => api.flowList(page, limit));
};

export const useFlow = (id: string) => {
  const api = useApi();
  return useQuery(['flow', id], () => api.flowById(id), {
    enabled: !!id
  });
};

export const useCreateFlow = () => {
  const api = useApi();
  const queryClient = useQueryClient();
  
  return useMutation(api.createFlow, {
    onSuccess: () => {
      queryClient.invalidateQueries(['flows']);
    }
  });
};

export const useCompileFlow = () => {
  const api = useApi();
  return useMutation(api.compileFlow);
};
```

## Phase 4: Canvas System Implementation

### 1. Canvas Store (Enhanced)
```typescript
// src/store/canvasStore.ts
import { create } from 'zustand';
import { subscribeWithSelector, devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface CanvasState {
  // Viewport state
  zoom: number;
  pan: { x: number; y: number };
  viewport: { width: number; height: number };
  
  // Interaction state
  mode: 'select' | 'connect' | 'pan' | 'add-node';
  selection: string[];
  isConnecting: boolean;
  connectionStart: Port | null;
  dragState: DragState | null;
  
  // Canvas data
  nodes: Record<string, FlowNode>;
  connections: Record<string, Connection>;
  
  // History for undo/redo
  history: CanvasSnapshot[];
  historyIndex: number;
  
  // Actions
  setViewport: (viewport: Partial<{ zoom: number; pan: { x: number; y: number } }>) => void;
  setMode: (mode: CanvasMode) => void;
  
  // Node operations
  addNode: (node: FlowNode) => void;
  updateNode: (id: string, updates: Partial<FlowNode>) => void;
  deleteNodes: (ids: string[]) => void;
  
  // Connection operations
  startConnection: (port: Port) => void;
  completeConnection: (port: Port) => void;
  cancelConnection: () => void;
  deleteConnection: (id: string) => void;
  
  // Selection operations
  selectNodes: (nodeIds: string[], additive?: boolean) => void;
  clearSelection: () => void;
  
  // History operations
  undo: () => void;
  redo: () => void;
  saveSnapshot: () => void;
  
  // Bulk operations
  loadFlow: (flow: Flow) => void;
  exportFlow: () => Flow;
  clearCanvas: () => void;
}

export const useCanvasStore = create<CanvasState>()(
  devtools(
    subscribeWithSelector(
      immer((set, get) => ({
        // Initial state
        zoom: 1,
        pan: { x: 0, y: 0 },
        viewport: { width: 0, height: 0 },
        mode: 'select',
        selection: [],
        isConnecting: false,
        connectionStart: null,
        dragState: null,
        nodes: {},
        connections: {},
        history: [],
        historyIndex: -1,
        
        // Viewport actions
        setViewport: (viewport) => set((state) => {
          if (viewport.zoom !== undefined) {
            state.zoom = Math.max(0.1, Math.min(3, viewport.zoom));
          }
          if (viewport.pan !== undefined) {
            state.pan = viewport.pan;
          }
        }),
        
        setMode: (mode) => set((state) => {
          state.mode = mode;
          if (mode !== 'connect') {
            state.isConnecting = false;
            state.connectionStart = null;
          }
        }),
        
        // Node operations
        addNode: (node) => set((state) => {
          state.nodes[node.id] = node;
          get().saveSnapshot();
        }),
        
        updateNode: (id, updates) => set((state) => {
          if (state.nodes[id]) {
            Object.assign(state.nodes[id], updates);
          }
        }),
        
        deleteNodes: (ids) => set((state) => {
          ids.forEach(id => {
            delete state.nodes[id];
            // Remove connections to/from deleted nodes
            Object.keys(state.connections).forEach(connId => {
              const conn = state.connections[connId];
              if (conn.source === id || conn.target === id) {
                delete state.connections[connId];
              }
            });
          });
          state.selection = state.selection.filter(id => !ids.includes(id));
          get().saveSnapshot();
        }),
        
        // Connection operations
        startConnection: (port) => set((state) => {
          state.isConnecting = true;
          state.connectionStart = port;
          state.mode = 'connect';
        }),
        
        completeConnection: (port) => set((state) => {
          if (!state.connectionStart) return;
          
          const connection: Connection = {
            id: `conn_${Date.now()}`,
            source: state.connectionStart.nodeId,
            target: port.nodeId,
            sourcePort: state.connectionStart.name,
            targetPort: port.name
          };
          
          state.connections[connection.id] = connection;
          state.isConnecting = false;
          state.connectionStart = null;
          state.mode = 'select';
          get().saveSnapshot();
        }),
        
        cancelConnection: () => set((state) => {
          state.isConnecting = false;
          state.connectionStart = null;
          state.mode = 'select';
        }),
        
        deleteConnection: (id) => set((state) => {
          delete state.connections[id];
          get().saveSnapshot();
        }),
        
        // Selection operations
        selectNodes: (nodeIds, additive = false) => set((state) => {
          if (additive) {
            state.selection = [...new Set([...state.selection, ...nodeIds])];
          } else {
            state.selection = nodeIds;
          }
        }),
        
        clearSelection: () => set((state) => {
          state.selection = [];
        }),
        
        // History operations
        saveSnapshot: () => set((state) => {
          const snapshot: CanvasSnapshot = {
            nodes: { ...state.nodes },
            connections: { ...state.connections },
            timestamp: Date.now()
          };
          
          // Remove future history if we're not at the end
          state.history = state.history.slice(0, state.historyIndex + 1);
          state.history.push(snapshot);
          state.historyIndex = state.history.length - 1;
          
          // Limit history size
          if (state.history.length > 50) {
            state.history = state.history.slice(-50);
            state.historyIndex = state.history.length - 1;
          }
        }),
        
        undo: () => set((state) => {
          if (state.historyIndex > 0) {
            state.historyIndex--;
            const snapshot = state.history[state.historyIndex];
            state.nodes = { ...snapshot.nodes };
            state.connections = { ...snapshot.connections };
          }
        }),
        
        redo: () => set((state) => {
          if (state.historyIndex < state.history.length - 1) {
            state.historyIndex++;
            const snapshot = state.history[state.historyIndex];
            state.nodes = { ...snapshot.nodes };
            state.connections = { ...snapshot.connections };
          }
        }),
        
        // Bulk operations
        loadFlow: (flow) => set((state) => {
          state.nodes = flow.nodes.reduce((acc, node) => ({ ...acc, [node.id]: node }), {});
          state.connections = flow.connections.reduce((acc, conn) => ({ ...acc, [conn.id]: conn }), {});
          state.selection = [];
          state.history = [];
          state.historyIndex = -1;
          get().saveSnapshot();
        }),
        
        exportFlow: (): Flow => {
          const state = get();
          return {
            id: '',
            name: '',
            nodes: Object.values(state.nodes),
            connections: Object.values(state.connections),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          };
        },
        
        clearCanvas: () => set((state) => {
          state.nodes = {};
          state.connections = {};
          state.selection = [];
          state.history = [];
          state.historyIndex = -1;
        })
      }))
    ),
    { name: 'canvas-store' }
  )
);
```

### 2. Canvas Interaction Hooks
```typescript
// src/utilities/hooks/useCanvasInteractions.ts
import { useCallback } from 'react';
import { useCanvasStore } from '@/store/canvasStore';

export const useCanvasInteractions = () => {
  const {
    mode,
    selection,
    updateNode,
    selectNodes,
    clearSelection,
    startConnection,
    completeConnection,
    cancelConnection
  } = useCanvasStore();
  
  const handleCanvasClick = useCallback((event: MouseEvent) => {
    if (mode === 'connect') {
      cancelConnection();
    } else {
      clearSelection();
    }
  }, [mode, cancelConnection, clearSelection]);
  
  const handleNodeClick = useCallback((nodeId: string, event: MouseEvent) => {
    event.stopPropagation();
    
    if (event.ctrlKey || event.metaKey) {
      // Additive selection
      const isSelected = selection.includes(nodeId);
      if (isSelected) {
        selectNodes(selection.filter(id => id !== nodeId));
      } else {
        selectNodes([...selection, nodeId]);
      }
    } else {
      selectNodes([nodeId]);
    }
  }, [selection, selectNodes]);
  
  const handleNodeDrag = useCallback((nodeId: string, offset: { x: number; y: number }) => {
    if (selection.includes(nodeId)) {
      // Move all selected nodes
      selection.forEach(id => {
        updateNode(id, (node) => ({
          position: {
            x: node.position.x + offset.x,
            y: node.position.y + offset.y
          }
        }));
      });
    } else {
      // Move only this node
      updateNode(nodeId, (node) => ({
        position: {
          x: node.position.x + offset.x,
          y: node.position.y + offset.y
        }
      }));
    }
  }, [selection, updateNode]);
  
  const handlePortClick = useCallback((port: Port, event: MouseEvent) => {
    event.stopPropagation();
    
    if (mode === 'connect' && connectionStart) {
      completeConnection(port);
    } else {
      startConnection(port);
    }
  }, [mode, connectionStart, startConnection, completeConnection]);
  
  return {
    handleCanvasClick,
    handleNodeClick,
    handleNodeDrag,
    handlePortClick
  };
};
```

This implementation guide provides a solid foundation for building the Flower frontend with the improved architecture inspired by Zeenome. The key advantages include:

1. **Component Resolution System** - Centralized, type-safe component access
2. **Auto-generated API Layer** - Consistent, maintainable API integration
3. **Enhanced State Management** - Powerful canvas state with history/undo
4. **Type Safety** - Comprehensive TypeScript coverage
5. **Modular Architecture** - Clear separation of concerns

The next steps would be implementing the remaining kit components, building the UI components (NodePalette, PropertyPanel, etc.), and adding the page-level components.