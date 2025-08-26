# Flower Component System Rules

## Component Resolution System

### Kit Components (Design System Primitives)
**NEVER import kit components directly. Always use Resolver.**

```typescript
// ❌ WRONG - Never do this
import { Button } from "@/components/kit/Button";
import { Canvas } from "@/components/kit/Canvas";

// ✅ CORRECT - Always use Resolver
import { Resolver } from "@/modules/resolver/Resolver";

const MyComponent = () => (
  <div>
    <Resolver.Button variant="primary">Save Flow</Resolver.Button>
    <Resolver.Canvas nodes={nodes} connections={connections} />
  </div>
);
```

### Available Kit Components

#### Form Elements
- `Resolver.Button` - All button variants and sizes
- `Resolver.Input` - Text inputs, textareas, number inputs
- `Resolver.Select` - Dropdown selects and multi-selects
- `Resolver.Checkbox` - Checkboxes and checkbox groups
- `Resolver.Radio` - Radio buttons and radio groups
- `Resolver.Switch` - Toggle switches
- `Resolver.Slider` - Range sliders

#### Canvas Elements
- `Resolver.Canvas` - Main canvas container
- `Resolver.Node` - Flow node component
- `Resolver.Connection` - Connection/edge component
- `Resolver.Port` - Input/output ports
- `Resolver.Handle` - Drag handles
- `Resolver.Grid` - Canvas grid background

#### Layout Components
- `Resolver.Card` - Content cards
- `Resolver.Panel` - Side panels and containers
- `Resolver.Toolbar` - Toolbar containers
- `Resolver.Sidebar` - Navigation sidebars
- `Resolver.Tabs` - Tab navigation
- `Resolver.Accordion` - Collapsible sections

#### Feedback Components
- `Resolver.Modal` - Modal dialogs
- `Resolver.Toast` - Toast notifications
- `Resolver.Alert` - Alert messages
- `Resolver.Loading` - Loading indicators
- `Resolver.Progress` - Progress bars
- `Resolver.Badge` - Status badges

#### Data Display
- `Resolver.Table` - Data tables
- `Resolver.List` - Lists and list items
- `Resolver.Tree` - Tree structures
- `Resolver.Avatar` - User avatars
- `Resolver.Image` - Optimized images

## Component Variants and Props

### Button Component
```typescript
<Resolver.Button
  variant="primary" | "secondary" | "ghost" | "destructive"
  size="sm" | "md" | "lg"
  disabled={boolean}
  loading={boolean}
  onClick={handleClick}
>
  Button Text
</Resolver.Button>
```

### Canvas Component
```typescript
<Resolver.Canvas
  zoom={number}
  pan={{ x: number, y: number }}
  mode="select" | "connect" | "pan" | "add-node"
  onCanvasClick={handleCanvasClick}
  onNodeAdd={handleNodeAdd}
  className={string}
>
  {/* Canvas content */}
</Resolver.Canvas>
```

### Node Component
```typescript
<Resolver.Node
  node={FlowNode}
  isSelected={boolean}
  isDragging={boolean}
  onDrag={handleDrag}
  onClick={handleClick}
  onDoubleClick={handleDoubleClick}
  onPortClick={handlePortClick}
/>
```

### Modal Component
```typescript
<Resolver.Modal
  isOpen={boolean}
  onClose={handleClose}
  title={string}
  size="sm" | "md" | "lg" | "xl"
  closeOnOverlayClick={boolean}
>
  {/* Modal content */}
</Resolver.Modal>
```

## UI Components (Composite Components)

### FlowCanvas
```typescript
// src/components/ui/FlowCanvas/FlowCanvas.tsx
import { Resolver } from "@/modules/resolver/Resolver";

export const FlowCanvas: React.FC<FlowCanvasProps> = ({
  flow,
  onNodeAdd,
  onNodeUpdate,
  onConnectionAdd
}) => {
  return (
    <Resolver.Canvas
      zoom={zoom}
      pan={pan}
      mode={mode}
      onCanvasClick={handleCanvasClick}
    >
      {/* Use kit components via Resolver */}
      {nodes.map(node => (
        <Resolver.Node
          key={node.id}
          node={node}
          isSelected={selection.includes(node.id)}
          onDrag={handleNodeDrag}
        />
      ))}
    </Resolver.Canvas>
  );
};
```

### NodePalette
```typescript
// src/components/ui/NodePalette/NodePalette.tsx
import { Resolver } from "@/modules/resolver/Resolver";

export const NodePalette: React.FC = () => {
  return (
    <Resolver.Panel className="node-palette">
      <Resolver.Input
        placeholder="Search nodes..."
        value={searchTerm}
        onChange={setSearchTerm}
      />
      
      <Resolver.Tabs value={activeCategory} onValueChange={setActiveCategory}>
        {categories.map(category => (
          <Resolver.List key={category}>
            {getNodesByCategory(category).map(nodeType => (
              <NodePaletteItem key={nodeType} nodeType={nodeType} />
            ))}
          </Resolver.List>
        ))}
      </Resolver.Tabs>
    </Resolver.Panel>
  );
};
```

## Component Development Rules

### Kit Component Development
1. **Location**: `src/components/kit/ComponentName/`
2. **Structure**:
   ```
   ComponentName/
   ├── ComponentName.tsx      # Main component
   ├── ComponentName.types.ts # Type definitions
   ├── ComponentName.test.tsx # Tests
   └── index.ts              # Exports
   ```
3. **Implementation**: Use Radix UI primitives + Tailwind CSS
4. **Variants**: Use `class-variance-authority` for variants
5. **Types**: Define in `src/contracts/components/`

### UI Component Development
1. **Location**: `src/components/ui/ComponentName/`
2. **Dependencies**: Only use kit components via Resolver
3. **Props**: Accept all necessary props for flexibility
4. **State**: Use local state or connect to stores
5. **Testing**: Test component behavior and interactions

### Page Component Development
1. **Location**: `src/app/**/_components/`
2. **Scope**: Only used within same page/route
3. **Dependencies**: Can use UI components and kit components (via Resolver)
4. **State**: Connect to relevant stores
5. **API**: Use API hooks for data fetching

## Styling Guidelines

### Tailwind CSS Classes
```typescript
// Use design system colors
className="bg-dominant-600 text-white hover:bg-dominant-700"

// Responsive design
className="flex flex-col md:flex-row lg:grid lg:grid-cols-3"

// Spacing and sizing
className="p-4 md:p-6 lg:p-8 w-full max-w-4xl mx-auto"
```

### Component Variants
```typescript
// Use class-variance-authority for variants
const buttonVariants = cva(
  "base-classes",
  {
    variants: {
      variant: {
        primary: "bg-dominant-600 text-white",
        secondary: "bg-gray-100 text-gray-900"
      },
      size: {
        sm: "px-3 py-1 text-sm",
        md: "px-4 py-2 text-base"
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md"
    }
  }
);
```

## Component Testing

### Kit Component Testing
```typescript
// Test component variants and props
describe('Button Component', () => {
  it('renders with primary variant', () => {
    render(<Button variant="primary">Test</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-dominant-600');
  });
  
  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Test</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### UI Component Testing
```typescript
// Test component behavior and interactions
describe('FlowCanvas', () => {
  it('renders nodes correctly', () => {
    const nodes = [createMockNode()];
    render(<FlowCanvas nodes={nodes} />);
    expect(screen.getByTestId('flow-node')).toBeInTheDocument();
  });
  
  it('handles node selection', () => {
    const onNodeSelect = jest.fn();
    render(<FlowCanvas onNodeSelect={onNodeSelect} />);
    fireEvent.click(screen.getByTestId('flow-node'));
    expect(onNodeSelect).toHaveBeenCalled();
  });
});
```

## Performance Optimization

### Component Memoization
```typescript
// Memoize expensive components
export const FlowNode = React.memo<FlowNodeProps>(({ node, isSelected }) => {
  // Component implementation
}, (prevProps, nextProps) => {
  // Custom comparison for optimal re-rendering
  return (
    prevProps.node.id === nextProps.node.id &&
    prevProps.isSelected === nextProps.isSelected &&
    JSON.stringify(prevProps.node.config) === JSON.stringify(nextProps.node.config)
  );
});
```

### Callback Optimization
```typescript
// Memoize callbacks to prevent unnecessary re-renders
const handleNodeClick = useCallback((nodeId: string) => {
  selectNode(nodeId);
}, [selectNode]);

const handleNodeDrag = useCallback((nodeId: string, offset: Point) => {
  updateNodePosition(nodeId, offset);
}, [updateNodePosition]);
```

### Virtual Rendering
```typescript
// Virtualize large lists of components
const VirtualizedNodeList = () => {
  const visibleNodes = useMemo(() => {
    return nodes.filter(node => isNodeVisible(node, viewport));
  }, [nodes, viewport]);
  
  return (
    <div>
      {visibleNodes.map(node => (
        <Resolver.Node key={node.id} node={node} />
      ))}
    </div>
  );
};
```