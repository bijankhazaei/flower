# Dify Web Project Structure Documentation

## Overview
Dify is a Next.js 15 application built with TypeScript, React 19, and Tailwind CSS. It's an open-source LLM application development platform with comprehensive internationalization support.

## Tech Stack
- **Framework**: Next.js 15.5.0 with App Router
- **Runtime**: Node.js >=22.11.0
- **Package Manager**: pnpm 10.15.0
- **Language**: TypeScript 5.8.3
- **UI**: React 19.1.1, Tailwind CSS 3.4.14
- **State Management**: Zustand, SWR, React Query
- **Testing**: Jest, React Testing Library
- **Linting**: ESLint 9, Oxlint
- **Build**: Standalone output for Docker deployment

## Project Structure

### Root Configuration Files
```
web/
├── package.json              # Dependencies and scripts
├── next.config.js           # Next.js configuration
├── tsconfig.json            # TypeScript configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── middleware.ts            # Next.js middleware for security
├── eslint.config.mjs        # ESLint configuration
├── jest.config.ts           # Jest testing configuration
├── postcss.config.js        # PostCSS configuration
└── Dockerfile               # Docker containerization
```

### Core Application Structure

#### App Directory (Next.js App Router)
```
app/
├── (commonLayout)/          # Shared layout for main app
│   ├── app/                 # App management pages
│   ├── apps/                # Apps listing page
│   ├── datasets/            # Dataset management
│   ├── explore/             # App marketplace
│   ├── plugins/             # Plugin management
│   ├── tools/               # Tools management
│   └── layout.tsx           # Common layout component
├── (shareLayout)/           # Layout for shared/public pages
│   ├── chat/[token]/        # Public chat interface
│   ├── chatbot/[token]/     # Embedded chatbot
│   ├── completion/[token]/  # Text completion interface
│   ├── workflow/[token]/    # Public workflow interface
│   └── layout.tsx           # Share layout component
├── account/                 # User account management
├── signin/                  # Authentication pages
├── components/              # Reusable React components
├── styles/                  # Global CSS styles
└── layout.tsx               # Root layout
```

#### Components Architecture
```
components/
├── app/                     # App-specific components
│   ├── annotation/          # Annotation management
│   ├── configuration/       # App configuration UI
│   ├── log/                 # Logging interfaces
│   └── overview/            # App overview dashboard
├── base/                    # Reusable UI components
│   ├── button/              # Button components
│   ├── input/               # Input components
│   ├── modal/               # Modal dialogs
│   ├── chat/                # Chat interfaces
│   ├── file-uploader/       # File upload components
│   └── icons/               # Icon components
├── datasets/                # Dataset-related components
├── workflow/                # Workflow builder components
├── plugins/                 # Plugin system components
└── tools/                   # Tools management components
```

#### Internationalization (i18n)
```
i18n/
├── en-US/                   # English translations
├── zh-Hans/                 # Simplified Chinese
├── zh-Hant/                 # Traditional Chinese
├── ja-JP/                   # Japanese
├── ko-KR/                   # Korean
├── es-ES/                   # Spanish
├── fr-FR/                   # French
├── de-DE/                   # German
├── pt-BR/                   # Portuguese (Brazil)
├── ru-RU/                   # Russian
├── it-IT/                   # Italian
├── th-TH/                   # Thai
├── vi-VN/                   # Vietnamese
├── pl-PL/                   # Polish
├── uk-UA/                   # Ukrainian
├── sl-SI/                   # Slovenian
├── ro-RO/                   # Romanian
├── hi-IN/                   # Hindi
└── fa-IR/                   # Persian
```

#### State Management & Services
```
context/                     # React Context providers
├── app-context.tsx          # App-wide state
├── dataset-detail.ts        # Dataset state
├── workspace-context.tsx    # Workspace state
└── modal-context.tsx        # Modal state management

service/                     # API service layer
├── apps.ts                  # App management APIs
├── datasets.ts              # Dataset APIs
├── workflow.ts              # Workflow APIs
├── plugins.ts               # Plugin APIs
└── knowledge/               # Knowledge base services

hooks/                       # Custom React hooks
├── use-breakpoints.ts       # Responsive design
├── use-i18n.ts             # Internationalization
├── use-theme.ts            # Theme management
└── use-workflow.ts         # Workflow operations
```

#### Utilities & Types
```
utils/                       # Utility functions
├── format.ts               # Data formatting
├── classnames.ts           # CSS class utilities
├── navigation.ts           # Navigation helpers
└── model-config.ts         # Model configuration

types/                      # TypeScript type definitions
├── app.ts                  # App-related types
├── workflow.ts             # Workflow types
└── feature.ts              # Feature types

models/                     # Data models
├── app.ts                  # App models
├── datasets.ts             # Dataset models
└── user.ts                 # User models
```

## Key Features Implementation

### 1. Multi-Layout Architecture
- **commonLayout**: Main authenticated app interface
- **shareLayout**: Public/embedded interfaces
- Route groups for layout organization

### 2. Comprehensive Component System
- **Base Components**: Reusable UI primitives
- **Feature Components**: Domain-specific components
- **Layout Components**: Page structure components

### 3. Internationalization Support
- 18+ language support
- Modular translation files
- RTL language support (Arabic, Persian)

### 4. State Management Strategy
- **Zustand**: Client-side state
- **SWR**: Server state caching
- **React Query**: Advanced server state
- **Context API**: Component tree state

### 5. Plugin Architecture
- Marketplace integration
- Custom plugin development
- Plugin authentication system
- Version management

### 6. Workflow Builder
- Visual workflow editor
- Node-based architecture
- Real-time collaboration
- Version history

## Development Patterns

### File Naming Conventions
- **Components**: PascalCase (e.g., `UserProfile.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useWorkflow.ts`)
- **Utilities**: camelCase (e.g., `formatDate.ts`)
- **Types**: PascalCase (e.g., `AppConfig.ts`)

### Component Structure
```typescript
// Component with props interface
interface ComponentProps {
  title: string
  onAction: () => void
}

export default function Component({ title, onAction }: ComponentProps) {
  return (
    <div className="component-container">
      {/* Component JSX */}
    </div>
  )
}
```

### API Service Pattern
```typescript
// Service layer with error handling
export const apiService = {
  async getData(id: string) {
    const response = await fetch(`/api/data/${id}`)
    if (!response.ok) throw new Error('Failed to fetch')
    return response.json()
  }
}
```

### Custom Hook Pattern
```typescript
// Reusable logic extraction
export function useFeature(config: FeatureConfig) {
  const [state, setState] = useState(initialState)
  
  useEffect(() => {
    // Effect logic
  }, [config])
  
  return { state, actions }
}
```

## Build & Deployment

### Development Scripts
```bash
pnpm dev                    # Development server
pnpm build                  # Production build
pnpm build:docker          # Docker-optimized build
pnpm lint                   # Code linting
pnpm test                   # Run tests
```

### Docker Configuration
- **Output**: Standalone for containerization
- **Multi-stage build**: Optimized for production
- **Static file handling**: Proper asset serving

### Environment Configuration
- **Development**: Local development setup
- **Production**: Optimized build with CSP headers
- **Docker**: Containerized deployment

## Security Features

### Content Security Policy
- Configurable CSP headers
- Nonce-based script execution
- XSS protection

### Authentication
- Multi-provider SSO support
- JWT token management
- Role-based access control

### Data Protection
- Input validation
- XSS prevention
- CSRF protection

## Performance Optimizations

### Code Splitting
- Route-based splitting
- Component lazy loading
- Dynamic imports

### Caching Strategy
- SWR for API caching
- Static asset caching
- Service worker integration

### Bundle Optimization
- Tree shaking
- Dead code elimination
- Asset optimization

## Testing Strategy

### Unit Testing
- Jest configuration
- React Testing Library
- Component testing patterns

### Integration Testing
- API integration tests
- Workflow testing
- E2E test preparation

## Usage with Amazon Q

This structure provides:
1. **Scalable Architecture**: Modular component system
2. **Type Safety**: Comprehensive TypeScript usage
3. **Internationalization**: Multi-language support patterns
4. **State Management**: Multiple state management approaches
5. **Modern Patterns**: Latest React and Next.js features
6. **Production Ready**: Docker deployment and security features

Use this structure as a reference for building similar LLM application platforms or complex React applications with Amazon Q assistance.