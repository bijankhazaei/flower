# Flower Frontend Architecture Rules

## Architecture Pattern
**Modular Monolith** with feature-based organization, clean separation of concerns, and component resolution system inspired by Zeenome.

## Component Categories & Import Rules

### 1. Kit Components (Design System)
- **Location**: `src/components/kit/`
- **Rule**: NEVER import directly
- **Usage**: Always use `Resolver` from `@/modules/resolver/Resolver`
- **Example**:
```typescript
// ❌ WRONG
import { Button } from "@/components/kit/Button";

// ✅ CORRECT
import { Resolver } from "@/modules/resolver/Resolver";
<Resolver.Button variant="primary">Save</Resolver.Button>
```

### 2. UI Components (Reusable)
- **Location**: `src/components/ui/`
- **Rule**: Can be imported directly anywhere
- **Purpose**: Composite components built with kit components

### 3. Layout Components
- **Location**: `src/components/layouts/`
- **Rule**: Used in page components and routing
- **Purpose**: Page structure and navigation

### 4. Page-specific Components
- **Location**: `src/app/**/_components/`
- **Rule**: Only used within same directory or parent page
- **Purpose**: Components specific to one page/route

## API Service Rules

### Action Files Pattern
- **Location**: `src/app/**/actions.tsx` or `src/services/apiService/*.actions.ts`
- **Purpose**: Define API endpoints with types
- **Auto-generation**: Methods automatically available in API service
- **Example**:
```typescript
export default (
  (api: ApiType.RawService) => ({
    flowList: (page = 1) => api.get<Flow[]>(`/flows?page=${page}`),
    createFlow: (flow: CreateFlowRequest) => api.post<Flow>('/flows', flow),
  })
) satisfies ApiActions;
```

### API Usage
- **CSR**: Use `useApi()` hook from `@/services/apiService/useApi`
- **SSR**: Use `Api` instance from `@/services/apiService`
- **Authentication**: Automatic token injection in CSR calls

## State Management Rules

### Store Types
- **Global App State**: Zustand (`src/store/appStore.ts`)
- **Canvas State**: Zustand with middleware (`src/store/canvasStore.ts`)
- **Atomic State**: Jotai atoms (`src/store/flowStore.ts`)
- **Observer Pattern**: Cross-component communication (`src/store/observerStore.ts`)

### Store Structure
```typescript
interface StoreState {
  // State properties
  data: DataType;
  
  // Actions (no separate actions object)
  updateData: (data: DataType) => void;
  resetData: () => void;
}
```

## Directory Structure Rules

### Naming Conventions
- **Components**: PascalCase (`FlowCanvas.tsx`)
- **Hooks**: camelCase starting with `use` (`useCanvasInteractions.ts`)
- **Stores**: camelCase ending with `Store` (`canvasStore.ts`)
- **Services**: camelCase ending with `Service` (`apiService/`)
- **Types**: PascalCase (`Flow`, `FlowNode`)

### File Organization
- **Index files**: Export all public APIs
- **Private files**: Prefix with `_` for internal use
- **Test files**: Co-located with `*.test.tsx` suffix
- **Type files**: Separate `.types.ts` files for complex types

## Configuration Rules

### Centralized Config
- **Location**: `src/configs/`
- **Access**: Via `AppConfig.section.key`
- **No direct env**: Never use `process.env` outside config files

### Environment Variables
```typescript
// src/configs/api.config.ts
export const ApiConfig = {
  baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: parseInt(process.env.REACT_APP_API_TIMEOUT || '10000'),
};
```

## Styling Rules

### Tailwind CSS Guidelines
- **Color Palette**: Only use approved design system colors
- **Responsive**: Mobile-first approach
- **Spacing**: Use consistent spacing scale
- **Typography**: Defined text scales and weights

### Design System Colors
```css
/* Approved colors only */
.bg-gray-{50-950}        /* Neutral */
.bg-dominant-{100-900}   /* Primary brand */
.bg-complement-{100-900} /* Success */
.bg-error-{100-900}      /* Error/danger */
.bg-information-{100-900} /* Info */
.bg-warning-{100-900}    /* Warning */
```

## Performance Rules

### Code Splitting
- **Route-based**: Lazy load page components
- **Feature-based**: Lazy load heavy features
- **Component-based**: Dynamic imports for large components

### Canvas Optimization
- **Virtualization**: Render only visible nodes
- **Memoization**: React.memo for expensive components
- **Debouncing**: Debounce frequent updates (pan, zoom)

## Testing Rules

### Test Structure
- **Unit tests**: Component behavior and logic
- **Integration tests**: Component interactions
- **E2E tests**: Complete user workflows

### Test Location
- **Co-located**: `Component.test.tsx` next to `Component.tsx`
- **Test utilities**: `src/utilities/testing/`
- **Mocks**: `src/__mocks__/`

## Security Rules

### Authentication
- **Token storage**: localStorage for CSR, no SSR access
- **Route protection**: AuthGuard component wrapper
- **API calls**: Automatic token injection

### Data Validation
- **Input validation**: Zod schemas for all forms
- **API validation**: Validate responses with types
- **XSS protection**: Sanitize user inputs