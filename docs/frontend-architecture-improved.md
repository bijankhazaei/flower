# Flower Frontend Architecture - Improved (Inspired by Zeenome)

## Architecture Pattern
**Modular Monolith** with feature-based organization, clean separation of concerns, and component resolution system.

## Directory Structure (Improved)
```
frontend/src/
├── app/                               # Next.js App Router (if using Next.js) or React Router
│   ├── (auth)/                        # Auth route group
│   │   ├── login/page.tsx             # Login page
│   │   └── register/page.tsx          # Registration page
│   ├── (dashboard)/                   # Main app route group
│   │   ├── flows/                     # Flow management
│   │   │   ├── page.tsx               # Flow list page
│   │   │   ├── [id]/page.tsx          # Flow editor page
│   │   │   └── _components/           # Page-specific components
│   │   ├── templates/                 # Template management
│   │   │   ├── page.tsx               # Template gallery
│   │   │   └── _components/
│   │   ├── nodes/                     # Node management
│   │   │   ├── page.tsx               # Node library
│   │   │   └── _components/
│   │   └── settings/                  # App settings
│   │       ├── page.tsx
│   │       └── _components/
│   └── actions.tsx                    # API endpoint definitions (auto-generated)
│
├── components/                        # Reusable components
│   ├── kit/                           # Core design system (NEVER import directly)
│   │   ├── Button/                    # Button component
│   │   ├── Input/                     # Input components
│   │   ├── Card/                      # Card component
│   │   ├── Modal/                     # Modal component
│   │   ├── Canvas/                    # Canvas primitives
│   │   └── [50+ UI components]        # Complete design system
│   ├── layouts/                       # Layout components
│   │   ├── BaseLayout.tsx             # Root layout
│   │   ├── AuthLayout.tsx             # Auth pages layout
│   │   ├── DashboardLayout.tsx        # Main app layout
│   │   └── EditorLayout.tsx           # Flow editor layout
│   └── ui/                            # Composite reusable components
│       ├── FlowCanvas/                # Canvas system
│       ├── NodePalette/               # Node palette
│       ├── PropertyPanel/             # Property editor
│       ├── Toolbar/                   # Editor toolbar
│       └── DataTable/                 # Advanced data tables
│
├── contracts/                         # Type definitions
│   ├── app/                           # Application contracts
│   │   ├── flow.ts                    # Flow types
│   │   ├── node.ts                    # Node types
│   │   └── apiActions.ts              # API action types
│   ├── base/                          # Base type utilities
│   ├── components/                    # Kit component interfaces
│   └── ui/                            # UI component types
│
├── services/                          # Business logic layer
│   ├── apiService/                    # HTTP client & API calls
│   │   ├── Api.ts                     # SSR API instance
│   │   ├── useApi.ts                  # CSR API hooks
│   │   ├── actions.ts                 # Auto-generated API methods
│   │   └── instantiateAxios.ts        # Axios configuration
│   ├── canvasService/                 # Canvas operations
│   ├── nodeService/                   # Node management
│   ├── flowService/                   # Flow operations
│   └── storageService/                # Local/session storage
│
├── store/                             # State management
│   ├── appStore.ts                    # Global app state (Zustand)
│   ├── canvasStore.ts                 # Canvas state (Zustand)
│   ├── flowStore.ts                   # Flow state (Jotai atoms)
│   └── observerStore.ts               # Observer pattern state
│
├── modules/                           # Feature modules
│   ├── auth/                          # Authentication module
│   │   ├── AuthGuard.tsx              # Route protection
│   │   └── useUser.ts                 # User management
│   ├── canvas/                        # Canvas system module
│   │   ├── CanvasEngine.tsx           # Core canvas logic
│   │   ├── NodeRenderer.tsx           # Node rendering
│   │   └── ConnectionManager.tsx      # Connection handling
│   └── resolver/                      # Kit component resolution
│       ├── Resolver.tsx               # Main resolver
│       └── ResolverBase.tsx           # Base resolver logic
│
├── utilities/                         # Helper functions
│   ├── helpers.ts                     # General utilities
│   ├── hooks.ts                       # Custom React hooks
│   ├── canvas.ts                      # Canvas utilities
│   ├── validation.ts                  # Zod schemas
│   └── transformations.ts             # Data transformers
│
├── configs/                           # Configuration files
│   ├── api.config.ts                  # API configuration
│   ├── app.config.ts                  # App configuration
│   └── index.ts                       # Unified exports
│
├── stylesheets/                       # Global styles
│   ├── global.scss                    # Global CSS
│   ├── _colors.scss                   # Color system
│   ├── _canvas.scss                   # Canvas-specific styles
│   └── _kit.scss                      # Kit component styles
│
└── locales/                           # Internationalization (optional)
    ├── en/                            # English translations
    └── [other languages]/             # Additional languages
```

## Component Resolution System (Inspired by Zeenome)

### Kit Components (Never Import Directly)
```typescript
// ❌ WRONG - Never import kit components directly
import { Button } from "@/components/kit/Button";

// ✅ CORRECT - Always use Resolver
import { Resolver } from "@/modules/resolver/Resolver";

const FlowEditor: React.FC = () => {
    return (
        <div className="flow-editor">
            <Resolver.Button variant="primary" size="md">
                Save Flow
            </Resolver.Button>
            <Resolver.Canvas 
                nodes={nodes}
                connections={connections}
                onNodeAdd={handleNodeAdd}
            />
        </div>
    );
};
```

### Available Kit Components
```typescript
// src/contracts/components/index.ts
export interface KitComponents {
    // Form Elements
    Button: ButtonComponent;
    Input: InputComponent;
    Select: SelectComponent;
    Checkbox: CheckboxComponent;
    
    // Canvas Elements
    Canvas: CanvasComponent;
    Node: NodeComponent;
    Connection: ConnectionComponent;
    Port: PortComponent;
    
    // Layout
    Card: CardComponent;
    Panel: PanelComponent;
    Toolbar: ToolbarComponent;
    Sidebar: SidebarComponent;
    
    // Feedback
    Modal: ModalComponent;
    Toast: ToastComponent;
    Loading: LoadingComponent;
    
    // Data Display
    Table: TableComponent;
    Tree: TreeComponent;
    List: ListComponent;
}
```

## API Service Architecture (Inspired by Zeenome)

### Action Files (Auto-generated API Methods)
```typescript
// src/app/flows/actions.tsx
import { ApiActions } from "@/contracts/app/apiActions";

export default (
    (api: ApiType.RawService) => ({
        // Flow operations
        flowList: (page = 1, limit = 10) =>
            api.get<Flow[]>(`/flows?page=${page}&limit=${limit}`),
        
        flowById: (id: string) =>
            api.get<Flow>(`/flows/${id}`),
        
        createFlow: (flow: CreateFlowRequest) =>
            api.post<Flow>('/flows', flow),
        
        updateFlow: (id: string, updates: UpdateFlowRequest) =>
            api.put<Flow>(`/flows/${id}`, updates),
        
        deleteFlow: (id: string) =>
            api.delete<void>(`/flows/${id}`),
        
        compileFlow: (flowDefinition: FlowDefinition) =>
            api.post<CompilationResult>('/compiler/compile', { flow_definition: flowDefinition }),
        
        executeFlow: (flowDefinition: FlowDefinition, inputs: any) =>
            api.post<ExecutionResult>('/compiler/execute', { flow_definition: flowDefinition, inputs }),
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
```

### API Usage Examples
```typescript
// CSR usage
"use client";
import { useApi } from "@/services/apiService/useApi";

const FlowList: React.FC = () => {
    const api = useApi();
    
    const fetchFlows = async () => {
        const result = await api.flowList(1, 20);
        if (result.ok) {
            setFlows(result.data);
        }
    };
    
    const compileFlow = async (flow: Flow) => {
        const result = await api.compileFlow({
            nodes: flow.nodes,
            connections: flow.connections
        });
        return result;
    };
};

// SSR usage
import { Api } from "@/services/apiService";

export default async function FlowPage({ params }: { params: { id: string } }) {
    const result = await Api.flowById(params.id);
    
    if (!result.ok) {
        redirect('/error/404');
    }
    
    return <FlowEditor flow={result.data} />;
}
```

## Canvas System Architecture

### Canvas Store (Zustand)
```typescript
// src/store/canvasStore.ts
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

interface CanvasState {
    // Viewport
    zoom: number;
    pan: { x: number; y: number };
    viewport: { width: number; height: number };
    
    // Selection
    selection: string[];
    selectionBox: SelectionBox | null;
    
    // Interaction modes
    mode: 'select' | 'connect' | 'pan' | 'add-node';
    isConnecting: boolean;
    connectionStart: Port | null;
    
    // Canvas data
    nodes: Record<string, FlowNode>;
    connections: Record<string, Connection>;
    
    // Actions
    setZoom: (zoom: number) => void;
    setPan: (pan: { x: number; y: number }) => void;
    setMode: (mode: CanvasMode) => void;
    
    // Node operations
    addNode: (node: FlowNode) => void;
    updateNode: (id: string, updates: Partial<FlowNode>) => void;
    deleteNode: (id: string) => void;
    
    // Connection operations
    startConnection: (port: Port) => void;
    completeConnection: (port: Port) => void;
    cancelConnection: () => void;
    
    // Selection operations
    selectNodes: (nodeIds: string[]) => void;
    clearSelection: () => void;
    
    // Bulk operations
    loadFlow: (flow: Flow) => void;
    clearCanvas: () => void;
}

export const useCanvasStore = create<CanvasState>()(
    subscribeWithSelector((set, get) => ({
        // Initial state
        zoom: 1,
        pan: { x: 0, y: 0 },
        viewport: { width: 0, height: 0 },
        selection: [],
        selectionBox: null,
        mode: 'select',
        isConnecting: false,
        connectionStart: null,
        nodes: {},
        connections: {},
        
        // Viewport actions
        setZoom: (zoom) => set({ zoom: Math.max(0.1, Math.min(3, zoom)) }),
        setPan: (pan) => set({ pan }),
        setMode: (mode) => set({ mode }),
        
        // Node operations
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
            const connections = Object.fromEntries(
                Object.entries(state.connections).filter(
                    ([_, conn]) => conn.source !== id && conn.target !== id
                )
            );
            return { nodes, connections };
        }),
        
        // Connection operations
        startConnection: (port) => set({
            isConnecting: true,
            connectionStart: port,
            mode: 'connect'
        }),
        
        completeConnection: (port) => set((state) => {
            if (!state.connectionStart) return state;
            
            const connection: Connection = {
                id: `conn_${Date.now()}`,
                source: state.connectionStart.nodeId,
                target: port.nodeId,
                sourcePort: state.connectionStart.name,
                targetPort: port.name
            };
            
            return {
                connections: { ...state.connections, [connection.id]: connection },
                isConnecting: false,
                connectionStart: null,
                mode: 'select'
            };
        }),
        
        cancelConnection: () => set({
            isConnecting: false,
            connectionStart: null,
            mode: 'select'
        }),
        
        // Selection operations
        selectNodes: (nodeIds) => set({ selection: nodeIds }),
        clearSelection: () => set({ selection: [] }),
        
        // Bulk operations
        loadFlow: (flow) => set({
            nodes: flow.nodes.reduce((acc, node) => ({ ...acc, [node.id]: node }), {}),
            connections: flow.connections.reduce((acc, conn) => ({ ...acc, [conn.id]: conn }), {}),
            selection: []
        }),
        
        clearCanvas: () => set({
            nodes: {},
            connections: {},
            selection: []
        })
    }))
);
```

### Canvas Component with Kit System
```typescript
// src/components/ui/FlowCanvas/FlowCanvas.tsx
"use client";
import React, { useCallback, useRef } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';
import { useCanvasInteractions } from '@/utilities/hooks';

export const FlowCanvas: React.FC = () => {
    const canvasRef = useRef<HTMLDivElement>(null);
    const {
        zoom,
        pan,
        nodes,
        connections,
        selection,
        mode,
        updateNode,
        selectNodes,
        clearSelection
    } = useCanvasStore();
    
    const {
        handleCanvasClick,
        handleNodeDrag,
        handleNodeClick,
        handleConnectionStart,
        handleConnectionEnd
    } = useCanvasInteractions();
    
    return (
        <div className="relative w-full h-full overflow-hidden bg-gray-50">
            {/* Canvas using Kit component */}
            <Resolver.Canvas
                ref={canvasRef}
                zoom={zoom}
                pan={pan}
                mode={mode}
                onCanvasClick={handleCanvasClick}
                className="absolute inset-0"
            >
                {/* Nodes layer */}
                {Object.values(nodes).map(node => (
                    <Resolver.Node
                        key={node.id}
                        node={node}
                        isSelected={selection.includes(node.id)}
                        onDrag={handleNodeDrag}
                        onClick={handleNodeClick}
                        onPortClick={handleConnectionStart}
                    />
                ))}
                
                {/* Connections layer */}
                {Object.values(connections).map(connection => (
                    <Resolver.Connection
                        key={connection.id}
                        connection={connection}
                        nodes={nodes}
                    />
                ))}
            </Resolver.Canvas>
            
            {/* Canvas controls */}
            <div className="absolute bottom-4 right-4 flex flex-col gap-2">
                <Resolver.Button
                    variant="secondary"
                    size="sm"
                    onClick={() => useCanvasStore.getState().setZoom(1)}
                >
                    Reset Zoom
                </Resolver.Button>
            </div>
        </div>
    );
};
```

## Key Improvements from Zeenome Architecture

### 1. **Component Resolution System**
- Never import kit components directly
- Centralized component access via Resolver
- Consistent API across all components
- Easy to swap implementations

### 2. **Auto-generated API Layer**
- Action files define endpoints
- Automatic method generation
- Type-safe API calls
- Separate SSR/CSR instances

### 3. **Feature-based Organization**
- Page-specific components in `_components`
- Clear separation of concerns
- Reusable components in `ui/`
- Kit components for design system

### 4. **Configuration Management**
- Centralized config files
- No direct `process.env` usage
- Structured configuration objects
- Environment-specific settings

### 5. **Type Safety**
- Comprehensive TypeScript coverage
- Contract-based interfaces
- Auto-generated types from API
- Strict validation with Zod

This improved architecture provides better maintainability, scalability, and developer experience while incorporating the best practices from the Zeenome project.