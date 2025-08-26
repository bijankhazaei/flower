# Flower Frontend Quick Start Guide

## Phase 1: MVP Implementation (First 4 weeks)

### Week 1: Project Setup & Basic Canvas

#### 1. Project Initialization
```bash
# Create new React app with TypeScript
npx create-react-app flower-frontend --template typescript
cd flower-frontend

# Install core dependencies
npm install @types/react @types/react-dom
npm install zustand react-query axios
npm install tailwindcss @headlessui/react
npm install react-hook-form @hookform/resolvers zod
npm install lucide-react clsx

# Install canvas dependencies
npm install react-flow-renderer
# OR for custom canvas:
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities

# Development dependencies
npm install -D @types/node @storybook/react vite
```

#### 2. Basic Project Structure
```
src/
├── components/
│   ├── ui/              # Base UI components
│   ├── canvas/          # Canvas-related components
│   ├── nodes/           # Node components
│   └── layout/          # Layout components
├── hooks/               # Custom hooks
├── stores/              # Zustand stores
├── services/            # API services
├── types/               # TypeScript types
└── utils/               # Utilities
```

#### 3. Core Types Definition
```typescript
// src/types/flow.ts
export interface FlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  config: Record<string, any>;
  inputs?: Record<string, any>;
  outputs?: Record<string, any>;
}

export interface Connection {
  id: string;
  source: string;
  target: string;
  sourcePort?: string;
  targetPort?: string;
}

export interface Flow {
  id: string;
  name: string;
  description?: string;
  nodes: FlowNode[];
  connections: Connection[];
  created_at: string;
  updated_at: string;
}

// src/types/node.ts
export interface NodeType {
  name: string;
  description: string;
  category: string;
  inputPorts: NodePort[];
  outputPorts: NodePort[];
  parameters: NodeParameter[];
}

export interface NodePort {
  name: string;
  data_type: string;
  required: boolean;
}

export interface NodeParameter {
  name: string;
  data_type: string;
  required: boolean;
  default?: any;
  description?: string;
}
```

#### 4. API Service Setup
```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

// src/services/flows.ts
import api from './api';
import { Flow } from '../types/flow';

export const flowsApi = {
  getAll: (): Promise<Flow[]> => 
    api.get('/flows/').then(res => res.data),
  
  getById: (id: string): Promise<Flow> => 
    api.get(`/flows/${id}`).then(res => res.data),
  
  create: (flow: Partial<Flow>): Promise<Flow> => 
    api.post('/flows/', flow).then(res => res.data),
  
  update: (id: string, flow: Partial<Flow>): Promise<Flow> => 
    api.put(`/flows/${id}`, flow).then(res => res.data),
  
  delete: (id: string): Promise<void> => 
    api.delete(`/flows/${id}`).then(res => res.data),
};

// src/services/nodes.ts
import api from './api';
import { NodeType } from '../types/node';

export const nodesApi = {
  getTypes: (): Promise<string[]> => 
    api.get('/nodes/types').then(res => res.data),
  
  getTypeInfo: (nodeType: string): Promise<NodeType> => 
    api.get(`/nodes/types/${nodeType}`).then(res => res.data),
  
  validate: (nodeType: string, config: any): Promise<any> => 
    api.post('/nodes/validate', { node_type: nodeType, config }).then(res => res.data),
};
```

### Week 2: Basic Canvas Implementation

#### 1. Canvas Store
```typescript
// src/stores/canvasStore.ts
import { create } from 'zustand';
import { FlowNode, Connection } from '../types/flow';

interface CanvasState {
  // Canvas state
  zoom: number;
  pan: { x: number; y: number };
  selection: string[];
  mode: 'select' | 'connect' | 'pan';
  
  // Flow data
  nodes: Record<string, FlowNode>;
  connections: Connection[];
  
  // Actions
  setZoom: (zoom: number) => void;
  setPan: (pan: { x: number; y: number }) => void;
  setSelection: (selection: string[]) => void;
  setMode: (mode: 'select' | 'connect' | 'pan') => void;
  
  addNode: (node: FlowNode) => void;
  updateNode: (id: string, updates: Partial<FlowNode>) => void;
  deleteNode: (id: string) => void;
  
  addConnection: (connection: Connection) => void;
  deleteConnection: (id: string) => void;
  
  clearCanvas: () => void;
  loadFlow: (nodes: FlowNode[], connections: Connection[]) => void;
}

export const useCanvasStore = create<CanvasState>((set, get) => ({
  // Initial state
  zoom: 1,
  pan: { x: 0, y: 0 },
  selection: [],
  mode: 'select',
  nodes: {},
  connections: [],
  
  // Actions
  setZoom: (zoom) => set({ zoom }),
  setPan: (pan) => set({ pan }),
  setSelection: (selection) => set({ selection }),
  setMode: (mode) => set({ mode }),
  
  addNode: (node) => set((state) => ({
    nodes: { ...state.nodes, [node.id]: node }
  })),
  
  updateNode: (id, updates) => set((state) => ({
    nodes: {
      ...state.nodes,
      [id]: { ...state.nodes[id], ...updates }
    }
  })),
  
  deleteNode: (id) => set((state) => {
    const { [id]: deleted, ...nodes } = state.nodes;
    const connections = state.connections.filter(
      conn => conn.source !== id && conn.target !== id
    );
    return { nodes, connections };
  }),
  
  addConnection: (connection) => set((state) => ({
    connections: [...state.connections, connection]
  })),
  
  deleteConnection: (id) => set((state) => ({
    connections: state.connections.filter(conn => conn.id !== id)
  })),
  
  clearCanvas: () => set({
    nodes: {},
    connections: [],
    selection: []
  }),
  
  loadFlow: (nodes, connections) => set({
    nodes: nodes.reduce((acc, node) => ({ ...acc, [node.id]: node }), {}),
    connections,
    selection: []
  }),
}));
```

#### 2. Basic Canvas Component
```typescript
// src/components/canvas/FlowCanvas.tsx
import React, { useRef, useCallback } from 'react';
import { useCanvasStore } from '../../stores/canvasStore';
import { FlowNode } from './FlowNode';
import { NodeConnection } from './NodeConnection';

interface FlowCanvasProps {
  className?: string;
}

export const FlowCanvas: React.FC<FlowCanvasProps> = ({ className }) => {
  const canvasRef = useRef<HTMLDivElement>(null);
  const { 
    zoom, 
    pan, 
    nodes, 
    connections, 
    selection,
    setSelection,
    updateNode 
  } = useCanvasStore();
  
  const handleCanvasClick = useCallback((e: React.MouseEvent) => {
    if (e.target === canvasRef.current) {
      setSelection([]);
    }
  }, [setSelection]);
  
  const handleNodeUpdate = useCallback((id: string, updates: Partial<FlowNode>) => {
    updateNode(id, updates);
  }, [updateNode]);
  
  return (
    <div 
      ref={canvasRef}
      className={`relative w-full h-full overflow-hidden bg-gray-50 ${className}`}
      onClick={handleCanvasClick}
    >
      <div
        className="absolute inset-0"
        style={{
          transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
          transformOrigin: '0 0'
        }}
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
        
        {/* Connections layer */}
        <svg className="absolute inset-0 pointer-events-none">
          {connections.map(connection => (
            <NodeConnection 
              key={connection.id} 
              connection={connection}
              nodes={nodes}
            />
          ))}
        </svg>
        
        {/* Nodes layer */}
        {Object.values(nodes).map(node => (
          <FlowNode
            key={node.id}
            node={node}
            isSelected={selection.includes(node.id)}
            onUpdate={handleNodeUpdate}
          />
        ))}
      </div>
    </div>
  );
};
```

#### 3. Basic Node Component
```typescript
// src/components/canvas/FlowNode.tsx
import React, { useCallback, useRef } from 'react';
import { FlowNode as FlowNodeType } from '../../types/flow';
import { useCanvasStore } from '../../stores/canvasStore';
import { useDraggable } from '../../hooks/useDraggable';

interface FlowNodeProps {
  node: FlowNodeType;
  isSelected: boolean;
  onUpdate: (id: string, updates: Partial<FlowNodeType>) => void;
}

export const FlowNode: React.FC<FlowNodeProps> = ({
  node,
  isSelected,
  onUpdate
}) => {
  const nodeRef = useRef<HTMLDivElement>(null);
  const { setSelection } = useCanvasStore();
  
  const handleDrag = useCallback((offset: { x: number; y: number }) => {
    onUpdate(node.id, {
      position: {
        x: node.position.x + offset.x,
        y: node.position.y + offset.y
      }
    });
  }, [node.id, node.position, onUpdate]);
  
  const { isDragging, dragHandlers } = useDraggable({
    onDrag: handleDrag
  });
  
  const handleClick = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    setSelection([node.id]);
  }, [node.id, setSelection]);
  
  return (
    <div
      ref={nodeRef}
      className={`
        absolute bg-white border-2 rounded-lg shadow-md cursor-pointer
        min-w-[150px] min-h-[80px]
        ${isSelected ? 'border-blue-500' : 'border-gray-300'}
        ${isDragging ? 'opacity-75' : ''}
        hover:shadow-lg transition-shadow
      `}
      style={{
        transform: `translate(${node.position.x}px, ${node.position.y}px)`
      }}
      onClick={handleClick}
      {...dragHandlers}
    >
      {/* Node Header */}
      <div className="px-3 py-2 bg-gray-100 rounded-t-lg border-b">
        <h3 className="text-sm font-medium text-gray-900">
          {node.type}
        </h3>
      </div>
      
      {/* Node Body */}
      <div className="p-3">
        <div className="text-xs text-gray-600">
          ID: {node.id}
        </div>
        {node.config && Object.keys(node.config).length > 0 && (
          <div className="mt-2 text-xs">
            <div className="font-medium">Config:</div>
            <pre className="text-gray-500">
              {JSON.stringify(node.config, null, 2)}
            </pre>
          </div>
        )}
      </div>
      
      {/* Input/Output ports will be added later */}
    </div>
  );
};
```

#### 4. Draggable Hook
```typescript
// src/hooks/useDraggable.ts
import { useCallback, useRef, useState } from 'react';

interface UseDraggableOptions {
  onDrag?: (offset: { x: number; y: number }) => void;
  onDragStart?: () => void;
  onDragEnd?: () => void;
}

export const useDraggable = ({
  onDrag,
  onDragStart,
  onDragEnd
}: UseDraggableOptions = {}) => {
  const [isDragging, setIsDragging] = useState(false);
  const dragStartPos = useRef<{ x: number; y: number } | null>(null);
  const lastPos = useRef<{ x: number; y: number } | null>(null);
  
  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsDragging(true);
    dragStartPos.current = { x: e.clientX, y: e.clientY };
    lastPos.current = { x: e.clientX, y: e.clientY };
    onDragStart?.();
    
    const handleMouseMove = (e: MouseEvent) => {
      if (lastPos.current) {
        const offset = {
          x: e.clientX - lastPos.current.x,
          y: e.clientY - lastPos.current.y
        };
        lastPos.current = { x: e.clientX, y: e.clientY };
        onDrag?.(offset);
      }
    };
    
    const handleMouseUp = () => {
      setIsDragging(false);
      dragStartPos.current = null;
      lastPos.current = null;
      onDragEnd?.();
      
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  }, [onDrag, onDragStart, onDragEnd]);
  
  return {
    isDragging,
    dragHandlers: {
      onMouseDown: handleMouseDown
    }
  };
};
```

### Week 3: Node Palette & Basic UI

#### 1. Node Palette Component
```typescript
// src/components/layout/NodePalette.tsx
import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { nodesApi } from '../../services/nodes';
import { Search, Plus } from 'lucide-react';

export const NodePalette: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const { data: nodeTypes, isLoading } = useQuery('nodeTypes', nodesApi.getTypes);
  
  const filteredNodes = nodeTypes?.filter(nodeType =>
    nodeType.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];
  
  const handleNodeDragStart = (nodeType: string) => {
    // Will implement drag to canvas
    console.log('Dragging node:', nodeType);
  };
  
  if (isLoading) {
    return <div className="p-4">Loading nodes...</div>;
  }
  
  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Nodes</h2>
        
        {/* Search */}
        <div className="mt-3 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Search nodes..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>
      
      {/* Node List */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-2">
          {filteredNodes.map(nodeType => (
            <div
              key={nodeType}
              className="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
              draggable
              onDragStart={() => handleNodeDragStart(nodeType)}
            >
              <div className="flex items-center space-x-2">
                <Plus className="w-4 h-4 text-gray-400" />
                <span className="text-sm font-medium text-gray-900">
                  {nodeType}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

#### 2. Main Layout Component
```typescript
// src/components/layout/MainLayout.tsx
import React from 'react';
import { NodePalette } from './NodePalette';
import { FlowCanvas } from '../canvas/FlowCanvas';
import { Toolbar } from './Toolbar';

export const MainLayout: React.FC = () => {
  return (
    <div className="h-screen flex flex-col">
      {/* Top Toolbar */}
      <Toolbar />
      
      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Left Sidebar - Node Palette */}
        <NodePalette />
        
        {/* Center - Canvas */}
        <div className="flex-1">
          <FlowCanvas />
        </div>
        
        {/* Right Sidebar - Properties (will add later) */}
      </div>
    </div>
  );
};
```

#### 3. Basic Toolbar
```typescript
// src/components/layout/Toolbar.tsx
import React from 'react';
import { Play, Save, Download, Upload } from 'lucide-react';

export const Toolbar: React.FC = () => {
  return (
    <div className="h-12 bg-white border-b border-gray-200 flex items-center px-4 space-x-4">
      <div className="flex items-center space-x-2">
        <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded">
          <Save className="w-4 h-4" />
        </button>
        <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded">
          <Upload className="w-4 h-4" />
        </button>
        <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded">
          <Download className="w-4 h-4" />
        </button>
      </div>
      
      <div className="w-px h-6 bg-gray-300" />
      
      <button className="flex items-center space-x-2 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">
        <Play className="w-4 h-4" />
        <span>Run Flow</span>
      </button>
    </div>
  );
};
```

### Week 4: Integration & Testing

#### 1. App Component with React Query
```typescript
// src/App.tsx
import React from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MainLayout } from './components/layout/MainLayout';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <MainLayout />
      </div>
    </QueryClientProvider>
  );
}

export default App;
```

#### 2. Basic Testing Setup
```typescript
// src/components/canvas/__tests__/FlowNode.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { FlowNode } from '../FlowNode';
import { FlowNode as FlowNodeType } from '../../../types/flow';

const mockNode: FlowNodeType = {
  id: 'test-node',
  type: 'TextInput',
  position: { x: 100, y: 100 },
  config: { placeholder: 'Enter text' }
};

describe('FlowNode', () => {
  it('renders node with correct type', () => {
    render(
      <FlowNode 
        node={mockNode} 
        isSelected={false} 
        onUpdate={jest.fn()} 
      />
    );
    
    expect(screen.getByText('TextInput')).toBeInTheDocument();
  });
  
  it('shows selected state', () => {
    render(
      <FlowNode 
        node={mockNode} 
        isSelected={true} 
        onUpdate={jest.fn()} 
      />
    );
    
    const nodeElement = screen.getByText('TextInput').closest('div');
    expect(nodeElement).toHaveClass('border-blue-500');
  });
});
```

## Next Steps (Weeks 5-8)

1. **Node Connections**: Implement port system and connection drawing
2. **Property Panel**: Add right sidebar for node configuration
3. **Flow Operations**: Save, load, compile, execute flows
4. **Real-time Updates**: WebSocket integration for live updates
5. **Advanced Canvas**: Zoom controls, selection box, copy/paste

## Quick Commands

```bash
# Start development server
npm start

# Run tests
npm test

# Build for production
npm run build

# Start Storybook (if added)
npm run storybook
```

This quick start guide provides a solid foundation for the first month of frontend development, focusing on the core canvas functionality and basic UI components.