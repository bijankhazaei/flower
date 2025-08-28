# Frontend Architecture Rules - React + TypeScript + Vite

## Tech Stack Requirements
- **Framework**: React 18.2.0+ with TypeScript 5.0+
- **Build Tool**: Vite 4.4.0+ with ESBuild
- **Styling**: Tailwind CSS 3.3.0+
- **State Management**: Zustand 5.0.8+, Jotai 2.13.1+
- **Data Fetching**: TanStack React Query 5.85.5+, Axios 1.6.0+
- **UI Components**: Radix UI, Lucide React, Framer Motion
- **Canvas**: ReactFlow 11.11.4+
- **Forms**: React Hook Form 7.62.0+ with Zod validation
- **Testing**: Vitest 3.2.4+, React Testing Library

## Mandatory Directory Structure
```
src/
├── components/kit/          # Design system components only
├── components/ui/           # Feature-specific UI components
├── pages/                   # Page components (one per route)
├── services/                # API services with axios
├── store/                   # Zustand stores only
├── hooks/                   # Custom React hooks
├── contracts/               # TypeScript interfaces/types
├── configs/                 # Configuration files
└── contexts/                # React Context providers
```

## Component Architecture Rules

### 1. Component Kit System (Required)
```typescript
// All kit components must follow this pattern
components/kit/ComponentName/
├── ComponentName.tsx        # Main component
├── ComponentName.types.ts   # TypeScript interfaces
└── index.ts                 # Export file
```

### 2. State Management Rules
- **Zustand**: For client-side state only
- **React Query**: For server state only
- **Context**: For component tree state only
- **No Redux or other state libraries**

### 3. Service Layer Pattern (Mandatory)
```typescript
// All API services must use this pattern
export const entityService = {
  getAll: () => api.get('/entity').then(res => res.data),
  create: (data: EntityData) => api.post('/entity', data).then(res => res.data),
  update: (id: string, data: Partial<EntityData>) => api.put(`/entity/${id}`, data).then(res => res.data),
  delete: (id: string) => api.delete(`/entity/${id}`).then(res => res.data),
}
```

## Development Standards

### File Naming (Enforced)
- **Components**: PascalCase (e.g., `UserProfile.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useCanvasStore.ts`)
- **Services**: camelCase with Service suffix (e.g., `projectService.ts`)
- **Types**: PascalCase (e.g., `FlowNode.ts`)

### Component Pattern (Required)
```typescript
interface ComponentProps {
  title: string
  onAction: () => void
  className?: string
}

export const Component: React.FC<ComponentProps> = ({ 
  title, 
  onAction, 
  className 
}) => {
  return (
    <div className={cn("base-styles", className)}>
      {/* Component JSX */}
    </div>
  )
}
```

### Custom Hook Pattern (Required)
```typescript
export const useFeature = (config: FeatureConfig) => {
  const [state, setState] = useState(initialState)
  
  const actions = useMemo(() => ({
    action1: () => setState(prev => ({ ...prev, /* update */ })),
    action2: () => { /* logic */ },
  }), [])
  
  return { state, actions }
}
```

## Performance Requirements

### Code Splitting (Mandatory)
- Route-based splitting with React.lazy
- Component splitting for large components
- Vendor chunking in Vite config

### State Optimization (Required)
- Zustand selectors for partial subscriptions
- React.memo for expensive components
- useMemo/useCallback for expensive computations

## Testing Requirements

### Unit Testing (Mandatory)
```typescript
describe('Component', () => {
  it('renders correctly', () => {
    render(<Component title="Test" onAction={jest.fn()} />)
    expect(screen.getByText('Test')).toBeInTheDocument()
  })
})
```

### Coverage Requirements
- Minimum 80% test coverage
- All custom hooks must be tested
- All service functions must be tested

## Build Configuration

### Vite Config (Required)
```typescript
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') }
  },
  build: {
    target: 'esnext',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog']
        }
      }
    }
  }
})
```

## Forbidden Patterns
- ❌ Class components (use function components only)
- ❌ Default exports for components (use named exports)
- ❌ Inline styles (use Tailwind classes only)
- ❌ Any state library other than Zustand
- ❌ Direct DOM manipulation (use React patterns)
- ❌ Untyped props (all props must have TypeScript interfaces)