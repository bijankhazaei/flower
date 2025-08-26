# Flower Frontend Architecture Guide

## Overview

The Flower frontend is a modern React application that provides a visual flow editor interface over the existing FastAPI backend. It follows component-based architecture with TypeScript for type safety and modern development practices.

## Architecture Principles

### 1. **Component-Driven Development**
- Atomic design methodology (Atoms → Molecules → Organisms → Templates → Pages)
- Reusable, composable components
- Storybook for component documentation and testing

### 2. **State Management Strategy**
- **Global State**: Zustand for app-wide state (user, flows, nodes)
- **Server State**: React Query for API data management and caching
- **Local State**: React hooks for component-specific state
- **Form State**: React Hook Form for complex forms

### 3. **Type Safety**
- TypeScript strict mode throughout
- API response types generated from backend schemas
- Component prop interfaces
- Event handler type safety

## Project Structure

```
frontend/src/
├── components/           # Reusable UI components
│   ├── atoms/           # Basic building blocks
│   ├── molecules/       # Component combinations
│   ├── organisms/       # Complex components
│   └── templates/       # Page layouts
├── pages/               # Route components
├── hooks/               # Custom React hooks
├── stores/              # Zustand stores
├── services/            # API services
├── types/               # TypeScript definitions
├── utils/               # Utility functions
├── styles/              # Global styles and themes
└── assets/              # Static assets
```

## Core Components Architecture

### Canvas System
```typescript
// Canvas hierarchy
<FlowCanvas>
  <CanvasViewport>
    <NodesLayer>
      <FlowNode />
      <FlowNode />
    </NodesLayer>
    <ConnectionsLayer>
      <NodeConnection />
    </ConnectionsLayer>
    <SelectionLayer>
      <SelectionBox />
    </SelectionLayer>
  </CanvasViewport>
  <CanvasControls>
    <ZoomControls />
    <PanControls />
  </CanvasControls>
</FlowCanvas>
```

### Node System
```typescript
// Node component structure
<FlowNode>
  <NodeHeader>
    <NodeIcon />
    <NodeTitle />
    <NodeMenu />
  </NodeHeader>
  <NodeBody>
    <InputPorts>
      <NodePort type="input" />
    </InputPorts>
    <NodeContent />
    <OutputPorts>
      <NodePort type="output" />
    </OutputPorts>
  </NodeBody>
  <NodeFooter>
    <NodeStatus />
  </NodeFooter>
</FlowNode>
```

## State Management

### Global Store Structure
```typescript
interface AppStore {
  // User state
  user: User | null;
  isAuthenticated: boolean;
  
  // Canvas state
  canvas: {
    zoom: number;
    pan: { x: number; y: number };
    selection: string[];
    mode: 'select' | 'connect' | 'pan';
  };
  
  // Flow state
  currentFlow: Flow | null;
  flows: Flow[];
  
  // Node state
  nodes: Record<string, FlowNode>;
  connections: Connection[];
  nodeTypes: NodeType[];
  
  // UI state
  sidebar: {
    isOpen: boolean;
    activeTab: 'nodes' | 'properties' | 'templates';
  };
  
  // Actions
  actions: {
    setUser: (user: User) => void;
    updateCanvas: (updates: Partial<CanvasState>) => void;
    addNode: (node: FlowNode) => void;
    updateNode: (id: string, updates: Partial<FlowNode>) => void;
    deleteNode: (id: string) => void;
    addConnection: (connection: Connection) => void;
    deleteConnection: (id: string) => void;
  };
}
```

### API Integration
```typescript
// React Query hooks for API integration
const useFlows = () => useQuery(['flows'], flowsApi.getAll);
const useFlow = (id: string) => useQuery(['flow', id], () => flowsApi.getById(id));
const useNodeTypes = () => useQuery(['nodeTypes'], nodesApi.getTypes);

// Mutations for data modification
const useCreateFlow = () => useMutation(flowsApi.create);
const useUpdateFlow = () => useMutation(flowsApi.update);
const useCompileFlow = () => useMutation(compilerApi.compile);
```

## Component Implementation Examples

### 1. Canvas Component
```typescript
interface CanvasProps {
  flow: Flow;
  onNodeAdd: (node: FlowNode) => void;
  onNodeUpdate: (id: string, updates: Partial<FlowNode>) => void;
  onConnectionAdd: (connection: Connection) => void;
}

const FlowCanvas: React.FC<CanvasProps> = ({
  flow,
  onNodeAdd,
  onNodeUpdate,
  onConnectionAdd
}) => {
  const canvasRef = useRef<HTMLDivElement>(null);
  const { zoom, pan, selection } = useCanvasStore();
  
  // Canvas interactions
  const { isDragging, dragOffset } = useDragAndDrop();
  const { isConnecting, connectionStart } = useConnectionMode();
  
  // Event handlers
  const handleNodeDrop = useCallback((nodeType: string, position: Point) => {
    const newNode = createNode(nodeType, position);
    onNodeAdd(newNode);
  }, [onNodeAdd]);
  
  const handleConnectionCreate = useCallback((start: Port, end: Port) => {
    const connection = createConnection(start, end);
    onConnectionAdd(connection);
  }, [onConnectionAdd]);
  
  return (
    <div 
      ref={canvasRef}
      className="canvas-container"
      style={{
        transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`
      }}
    >
      <NodesLayer 
        nodes={flow.nodes}
        onNodeUpdate={onNodeUpdate}
        selection={selection}
      />
      <ConnectionsLayer 
        connections={flow.connections}
        isConnecting={isConnecting}
        connectionStart={connectionStart}
      />
      <SelectionLayer selection={selection} />
    </div>
  );
};
```

### 2. Node Component
```typescript
interface NodeProps {
  node: FlowNode;
  isSelected: boolean;
  onUpdate: (updates: Partial<FlowNode>) => void;
  onSelect: () => void;
}

const FlowNode: React.FC<NodeProps> = ({
  node,
  isSelected,
  onUpdate,
  onSelect
}) => {
  const nodeRef = useRef<HTMLDivElement>(null);
  const { nodeType } = useNodeType(node.type);
  
  // Drag handling
  const { isDragging, dragHandlers } = useDraggable({
    onDrag: (offset) => onUpdate({ position: offset }),
    onDragEnd: () => {/* save position */}
  });
  
  // Port connection handling
  const { connectHandlers } = usePortConnection({
    onConnectionStart: (port) => {/* start connection */},
    onConnectionEnd: (port) => {/* complete connection */}
  });
  
  return (
    <div
      ref={nodeRef}
      className={cn(
        'flow-node',
        isSelected && 'selected',
        isDragging && 'dragging'
      )}
      style={{
        transform: `translate(${node.position.x}px, ${node.position.y}px)`
      }}
      onClick={onSelect}
      {...dragHandlers}
    >
      <NodeHeader 
        title={nodeType?.name || node.type}
        icon={nodeType?.icon}
        menu={<NodeContextMenu node={node} />}
      />
      
      <NodeBody>
        <InputPorts 
          ports={nodeType?.inputPorts || []}
          values={node.inputs}
          {...connectHandlers}
        />
        
        <NodeContent>
          {node.config && (
            <NodeParameters 
              parameters={nodeType?.parameters || []}
              values={node.config}
              onChange={(config) => onUpdate({ config })}
            />
          )}
        </NodeContent>
        
        <OutputPorts 
          ports={nodeType?.outputPorts || []}
          {...connectHandlers}
        />
      </NodeBody>
      
      <NodeFooter>
        <NodeStatus status={node.status} />
      </NodeFooter>
    </div>
  );
};
```

### 3. Node Palette
```typescript
const NodePalette: React.FC = () => {
  const { data: nodeTypes } = useNodeTypes();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  
  // Filter nodes based on search and category
  const filteredNodes = useMemo(() => {
    return nodeTypes?.filter(node => {
      const matchesSearch = node.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = !selectedCategory || node.category === selectedCategory;
      return matchesSearch && matchesCategory;
    }) || [];
  }, [nodeTypes, searchTerm, selectedCategory]);
  
  // Group nodes by category
  const nodesByCategory = useMemo(() => {
    return groupBy(filteredNodes, 'category');
  }, [filteredNodes]);
  
  return (
    <div className="node-palette">
      <PaletteHeader>
        <SearchInput 
          value={searchTerm}
          onChange={setSearchTerm}
          placeholder="Search nodes..."
        />
        <CategoryFilter 
          categories={Object.keys(nodesByCategory)}
          selected={selectedCategory}
          onChange={setSelectedCategory}
        />
      </PaletteHeader>
      
      <PaletteContent>
        {Object.entries(nodesByCategory).map(([category, nodes]) => (
          <NodeCategory key={category} title={category}>
            {nodes.map(nodeType => (
              <DraggableNodeItem 
                key={nodeType.name}
                nodeType={nodeType}
                onDragStart={() => {/* start drag */}}
              />
            ))}
          </NodeCategory>
        ))}
      </PaletteContent>
    </div>
  );
};
```

## Custom Hooks

### Canvas Interactions
```typescript
// Drag and drop hook
const useDragAndDrop = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  
  const dragHandlers = useMemo(() => ({
    onMouseDown: (e: MouseEvent) => {
      setIsDragging(true);
      // Calculate initial offset
    },
    onMouseMove: (e: MouseEvent) => {
      if (isDragging) {
        setDragOffset({ x: e.clientX, y: e.clientY });
      }
    },
    onMouseUp: () => {
      setIsDragging(false);
    }
  }), [isDragging]);
  
  return { isDragging, dragOffset, dragHandlers };
};

// Connection mode hook
const useConnectionMode = () => {
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionStart, setConnectionStart] = useState<Port | null>(null);
  
  const startConnection = useCallback((port: Port) => {
    setIsConnecting(true);
    setConnectionStart(port);
  }, []);
  
  const endConnection = useCallback((port: Port) => {
    if (connectionStart) {
      // Create connection
      setIsConnecting(false);
      setConnectionStart(null);
    }
  }, [connectionStart]);
  
  return { isConnecting, connectionStart, startConnection, endConnection };
};
```

### API Integration
```typescript
// Flow management hooks
const useFlowOperations = () => {
  const queryClient = useQueryClient();
  
  const createFlow = useMutation(flowsApi.create, {
    onSuccess: () => {
      queryClient.invalidateQueries(['flows']);
    }
  });
  
  const updateFlow = useMutation(flowsApi.update, {
    onSuccess: (data) => {
      queryClient.setQueryData(['flow', data.id], data);
    }
  });
  
  const deleteFlow = useMutation(flowsApi.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries(['flows']);
    }
  });
  
  return { createFlow, updateFlow, deleteFlow };
};

// Real-time updates hook
const useRealtimeUpdates = (flowId: string) => {
  const [socket] = useState(() => io('/flows'));
  
  useEffect(() => {
    socket.emit('join-flow', flowId);
    
    socket.on('flow-updated', (update) => {
      // Handle real-time flow updates
    });
    
    socket.on('user-joined', (user) => {
      // Handle user presence
    });
    
    return () => {
      socket.emit('leave-flow', flowId);
      socket.disconnect();
    };
  }, [flowId, socket]);
  
  return socket;
};
```

## Performance Optimization

### Canvas Virtualization
```typescript
const VirtualizedCanvas: React.FC<CanvasProps> = ({ nodes, connections }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [viewport, setViewport] = useState({ x: 0, y: 0, width: 0, height: 0 });
  
  // Calculate visible nodes based on viewport
  const visibleNodes = useMemo(() => {
    return nodes.filter(node => {
      return isNodeInViewport(node, viewport);
    });
  }, [nodes, viewport]);
  
  // Update viewport on scroll/zoom
  useEffect(() => {
    const updateViewport = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setViewport({
          x: rect.left,
          y: rect.top,
          width: rect.width,
          height: rect.height
        });
      }
    };
    
    updateViewport();
    window.addEventListener('resize', updateViewport);
    return () => window.removeEventListener('resize', updateViewport);
  }, []);
  
  return (
    <div ref={containerRef} className="virtualized-canvas">
      {visibleNodes.map(node => (
        <FlowNode key={node.id} node={node} />
      ))}
    </div>
  );
};
```

### Memoization Strategy
```typescript
// Memoized node component
const FlowNode = React.memo<NodeProps>(({ node, isSelected, onUpdate }) => {
  // Component implementation
}, (prevProps, nextProps) => {
  // Custom comparison for optimal re-rendering
  return (
    prevProps.node.id === nextProps.node.id &&
    prevProps.isSelected === nextProps.isSelected &&
    JSON.stringify(prevProps.node.config) === JSON.stringify(nextProps.node.config)
  );
});

// Memoized connection component
const NodeConnection = React.memo<ConnectionProps>(({ connection }) => {
  // Connection rendering logic
}, (prevProps, nextProps) => {
  return prevProps.connection.id === nextProps.connection.id;
});
```

## Testing Strategy

### Component Testing
```typescript
// Node component test
describe('FlowNode', () => {
  it('renders node with correct title', () => {
    const node = createMockNode({ type: 'TextInput' });
    render(<FlowNode node={node} onUpdate={jest.fn()} />);
    
    expect(screen.getByText('Text Input')).toBeInTheDocument();
  });
  
  it('handles drag interactions', async () => {
    const onUpdate = jest.fn();
    const node = createMockNode();
    
    render(<FlowNode node={node} onUpdate={onUpdate} />);
    
    const nodeElement = screen.getByRole('button');
    await userEvent.drag(nodeElement, { delta: { x: 100, y: 50 } });
    
    expect(onUpdate).toHaveBeenCalledWith({
      position: { x: 100, y: 50 }
    });
  });
});
```

### Integration Testing
```typescript
// Canvas integration test
describe('FlowCanvas Integration', () => {
  it('creates connection between nodes', async () => {
    const flow = createMockFlow();
    const onConnectionAdd = jest.fn();
    
    render(
      <FlowCanvas 
        flow={flow} 
        onConnectionAdd={onConnectionAdd}
      />
    );
    
    // Simulate connection creation
    const outputPort = screen.getByTestId('output-port-1');
    const inputPort = screen.getByTestId('input-port-2');
    
    await userEvent.dragAndDrop(outputPort, inputPort);
    
    expect(onConnectionAdd).toHaveBeenCalledWith(
      expect.objectContaining({
        source: 'node-1',
        target: 'node-2'
      })
    );
  });
});
```

This architecture provides a solid foundation for building a modern, performant, and maintainable visual flow editor that integrates seamlessly with the existing Flower backend.