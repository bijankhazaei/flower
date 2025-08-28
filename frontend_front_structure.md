# Flower Frontend Structure - React + TypeScript + Vite

## Overview
Flower Frontend is a modern React 18 application built with TypeScript, Vite, and Tailwind CSS. It provides a visual flow builder interface for AI workflow orchestration with real-time collaboration features.

## Tech Stack
- **Framework**: React 18.2.0 with TypeScript 5.0+
- **Build Tool**: Vite 4.4.0 with ESBuild
- **Styling**: Tailwind CSS 3.3.0
- **State Management**: Zustand 5.0.8, Jotai 2.13.1
- **Data Fetching**: TanStack React Query 5.85.5, Axios 1.6.0
- **UI Components**: Radix UI, Lucide React, Framer Motion
- **Canvas**: ReactFlow 11.11.4
- **Forms**: React Hook Form 7.62.0 with Zod validation
- **Testing**: Vitest 3.2.4, React Testing Library

## Project Structure

### Root Configuration
```
frontend/
├── package.json              # Dependencies and scripts
├── vite.config.ts           # Vite configuration with proxy
├── tsconfig.json            # TypeScript configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── eslint.config.js         # ESLint configuration
├── vitest.config.ts         # Vitest testing configuration
├── postcss.config.js        # PostCSS configuration
├── .prettierrc              # Prettier formatting
└── Dockerfile               # Docker containerization
```

### Source Structure
```
src/
├── app/                     # Application-level logic
│   └── actions.ts           # Global actions/reducers
├── components/              # Reusable components
│   ├── kit/                 # Design system components
│   │   ├── Button/          # Button component variants
│   │   ├── Canvas/          # Canvas container component
│   │   ├── Card/            # Card layout component
│   │   ├── Connection/      # Flow connection component
│   │   ├── Input/           # Input field components
│   │   ├── Modal/           # Modal dialog component
│   │   └── Node/            # Flow node component
│   ├── layouts/             # Layout components
│   ├── ui/                  # Feature-specific UI components
│   │   ├── FlowCanvas/      # Main canvas for flow editing
│   │   ├── FlowCompiler/    # Flow compilation interface
│   │   ├── FlowExecutor/    # Flow execution controls
│   │   ├── FlowList/        # Flow listing component
│   │   ├── NodePalette/     # Node selection palette
│   │   ├── PropertyPanel/   # Node property editor
│   │   └── Toolbar/         # Main toolbar component
│   ├── Layout.tsx           # Main application layout
│   └── ProtectedRoute.tsx   # Authentication wrapper
├── configs/                 # Configuration files
│   ├── app.config.ts        # Application configuration
│   └── index.ts             # Config exports
├── contexts/                # React Context providers
│   └── AuthContext.tsx      # Authentication context
├── contracts/               # TypeScript interfaces/types
│   ├── api/                 # API response types
│   │   └── index.ts
│   ├── app/                 # Application types
│   ├── base/                # Base/common types
│   ├── components/          # Component prop types
│   │   └── index.ts
│   └── ui/                  # UI-specific types
├── hooks/                   # Custom React hooks
│   └── useCanvasInteractions.ts # Canvas interaction logic
├── modules/                 # Feature modules
│   ├── auth/                # Authentication module
│   ├── canvas/              # Canvas functionality
│   └── resolver/            # Module resolver
│       └── Resolver.tsx
├── pages/                   # Page components
│   ├── Dashboard.tsx        # Main dashboard
│   ├── FlowEditor.tsx       # Flow editing interface
│   ├── Login.tsx            # Login page
│   ├── Projects.tsx         # Project management
│   └── Users.tsx            # User management
├── services/                # API services
│   ├── apiService/          # Generic API utilities
│   │   ├── index.ts
│   │   └── useApi.ts        # API hooks
│   ├── canvasService/       # Canvas-specific services
│   ├── flowService/         # Flow management services
│   ├── nodeService/         # Node management services
│   └── api.ts               # Main API configuration
├── store/                   # State management
│   └── canvasStore.ts       # Canvas state with Zustand
├── stylesheets/             # Global styles
├── test/                    # Testing utilities
│   ├── setup.ts             # Test setup
│   └── utils.tsx            # Test utilities
├── types/                   # Global TypeScript types
├── utilities/               # Utility functions
│   └── helpers.ts           # Helper functions
├── utils/                   # Additional utilities
├── App.tsx                  # Main App component
├── App.css                  # App-specific styles
├── index.css                # Global styles
└── main.tsx                 # Application entry point
```

## Key Architecture Patterns

### 1. Component Kit System
```typescript
// Design system approach with consistent components
components/kit/
├── Button/
│   ├── Button.tsx           # Main button component
│   ├── Button.types.ts      # Button prop types
│   └── Button.stories.tsx   # Storybook stories
```

### 2. State Management Strategy
```typescript
// Zustand for canvas state
export const useCanvasStore = create<CanvasState>((set, get) => ({
  nodes: {},
  connections: {},
  selection: [],
  addNode: (node) => set((state) => ({
    nodes: { ...state.nodes, [node.id]: node }
  })),
  // ... other actions
}))
```

### 3. Service Layer Pattern
```typescript
// API services with axios
export const projectService = {
  getAll: () => api.get('/projects').then(res => res.data),
  create: (data: any) => api.post('/projects', data).then(res => res.data),
  update: (id: string, data: any) => api.put(`/projects/${id}`, data).then(res => res.data),
}
```

### 4. Custom Hooks Pattern
```typescript
// Canvas interactions hook
export const useCanvasInteractions = () => {
  const { nodes, connections, addNode } = useCanvasStore()
  
  const handleNodeDrop = useCallback((nodeType: string, position: Point) => {
    // Node drop logic
  }, [addNode])
  
  return { handleNodeDrop, /* other handlers */ }
}
```

## Feature Implementation

### 1. Visual Flow Editor
- **ReactFlow Integration**: Canvas-based flow editing
- **Node Palette**: Drag-and-drop node creation
- **Property Panel**: Node configuration interface
- **Connection System**: Visual flow connections

### 2. Real-time Collaboration
- **WebSocket Integration**: Live updates
- **Conflict Resolution**: Merge strategies
- **User Presence**: Show active users
- **Version Control**: Flow history tracking

### 3. Project Management
- **Project Hierarchy**: Organize flows by project
- **User Permissions**: Role-based access
- **Sharing**: Project collaboration features
- **Templates**: Reusable flow templates

### 4. Authentication System
- **JWT Integration**: Token-based auth
- **Protected Routes**: Route guards
- **Role Management**: User role handling
- **Session Management**: Auto-refresh tokens

## Development Patterns

### Component Structure
```typescript
// Consistent component pattern
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
      <h2>{title}</h2>
      <button onClick={onAction}>Action</button>
    </div>
  )
}
```

### API Integration
```typescript
// React Query integration
export const useProjects = () => {
  return useQuery({
    queryKey: ['projects'],
    queryFn: projectService.getAll,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}
```

### Form Handling
```typescript
// React Hook Form with Zod validation
const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().optional(),
})

export const ProjectForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  })
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  )
}
```

## Build & Development

### Development Scripts
```bash
npm run dev                  # Development server with HMR
npm run build               # Production build
npm run preview             # Preview production build
npm run lint                # ESLint checking
npm run lint:fix            # Auto-fix linting issues
npm run format              # Prettier formatting
npm run type-check          # TypeScript checking
npm run test                # Run tests with Vitest
npm run test:ui             # Vitest UI interface
```

### Vite Configuration
```typescript
// Optimized build configuration
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'esnext',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-select'],
        },
      },
    },
  },
})
```

## Performance Optimizations

### Code Splitting
- **Route-based splitting**: Lazy load pages
- **Component splitting**: Dynamic imports
- **Vendor chunking**: Separate vendor bundles

### State Optimization
- **Selective subscriptions**: Zustand selectors
- **Memoization**: React.memo, useMemo, useCallback
- **Virtual scrolling**: Large lists optimization

### Bundle Analysis
- **Tree shaking**: Remove unused code
- **Asset optimization**: Image and font optimization
- **Compression**: Gzip/Brotli compression

## Testing Strategy

### Unit Testing
```typescript
// Component testing with React Testing Library
describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
})
```

### Integration Testing
- **API integration**: Mock API responses
- **User workflows**: Complete user journeys
- **Canvas interactions**: Flow editor testing

### E2E Testing
- **Critical paths**: User authentication flow
- **Flow creation**: Complete flow building
- **Collaboration**: Multi-user scenarios

## Deployment

### Docker Configuration
```dockerfile
# Multi-stage build for optimization
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
```

### Environment Variables
```bash
VITE_API_URL=http://localhost:8022
VITE_WS_URL=ws://localhost:8022
VITE_APP_NAME=Flower
```

This structure provides a scalable, maintainable frontend architecture that supports the complex requirements of a visual flow builder while maintaining excellent developer experience and performance.