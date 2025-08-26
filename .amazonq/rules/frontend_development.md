# Flower Frontend Development Guidelines

## Development Workflow

### 1. Component Development Process
1. **Design First**: Create component interface in `contracts/`
2. **Kit Component**: Implement in `kit/` if reusable primitive
3. **UI Component**: Build composite component in `ui/`
4. **Integration**: Add to Resolver if kit component
5. **Testing**: Write unit and integration tests
6. **Documentation**: Update component documentation

### 2. Feature Development Process
1. **API Actions**: Define endpoints in `actions.tsx`
2. **Types**: Create interfaces in `contracts/`
3. **Store**: Set up state management if needed
4. **Components**: Build UI components
5. **Pages**: Create page components
6. **Integration**: Connect API, state, and UI
7. **Testing**: End-to-end feature testing

## Code Quality Standards

### TypeScript Rules
- **Strict mode**: Enable all strict TypeScript options
- **No any**: Avoid `any` type, use proper interfaces
- **Explicit returns**: Always specify return types for functions
- **Null safety**: Handle null/undefined cases explicitly

### React Best Practices
- **Functional components**: Use function components with hooks
- **Custom hooks**: Extract reusable logic into hooks
- **Memoization**: Use React.memo, useMemo, useCallback appropriately
- **Error boundaries**: Implement error boundaries for robust UX

### Performance Guidelines
- **Bundle size**: Keep bundle size under 1MB gzipped
- **Lazy loading**: Implement code splitting for routes and features
- **Image optimization**: Use WebP format and lazy loading
- **Canvas performance**: Virtualize large node lists

## Canvas System Guidelines

### Canvas Architecture
- **Layered rendering**: Separate layers for nodes, connections, UI
- **Event handling**: Efficient event delegation and bubbling
- **State management**: Centralized canvas state with Zustand
- **Undo/Redo**: Built-in history management

### Canvas Performance
- **Viewport culling**: Only render visible elements
- **Debounced updates**: Debounce pan/zoom operations
- **Memoized components**: Prevent unnecessary re-renders
- **Efficient selections**: Optimize selection algorithms

### Canvas Interactions
- **Mouse events**: Handle drag, click, hover efficiently
- **Keyboard shortcuts**: Implement standard shortcuts (Ctrl+Z, Ctrl+C, etc.)
- **Touch support**: Mobile-friendly touch interactions
- **Accessibility**: Keyboard navigation and screen reader support

## API Integration Guidelines

### Request/Response Handling
- **Loading states**: Show loading indicators for async operations
- **Error handling**: Graceful error handling with user feedback
- **Retry logic**: Implement retry for failed requests
- **Caching**: Use React Query for intelligent caching

### Real-time Features
- **WebSocket**: Use Socket.io for real-time updates
- **Optimistic updates**: Update UI before server confirmation
- **Conflict resolution**: Handle concurrent editing conflicts
- **Connection management**: Robust connection handling

## Testing Strategy

### Unit Testing
- **Component testing**: Test component behavior and props
- **Hook testing**: Test custom hooks in isolation
- **Utility testing**: Test helper functions and utilities
- **Store testing**: Test state management logic

### Integration Testing
- **API integration**: Test API service layer
- **Component integration**: Test component interactions
- **Canvas testing**: Test canvas operations and interactions
- **Flow testing**: Test complete user workflows

### E2E Testing
- **User journeys**: Test complete user workflows
- **Cross-browser**: Test on multiple browsers
- **Performance**: Test performance under load
- **Accessibility**: Test with screen readers and keyboard navigation

## Deployment Guidelines

### Build Optimization
- **Tree shaking**: Remove unused code
- **Code splitting**: Split code by routes and features
- **Asset optimization**: Optimize images, fonts, and other assets
- **Bundle analysis**: Regular bundle size analysis

### Environment Configuration
- **Environment variables**: Proper environment variable management
- **Feature flags**: Use feature flags for gradual rollouts
- **Error tracking**: Implement error tracking and monitoring
- **Performance monitoring**: Track performance metrics

## Accessibility Guidelines

### WCAG Compliance
- **Keyboard navigation**: Full keyboard accessibility
- **Screen readers**: Proper ARIA labels and semantic HTML
- **Color contrast**: Meet WCAG AA color contrast requirements
- **Focus management**: Proper focus management and indicators

### Canvas Accessibility
- **Keyboard navigation**: Navigate canvas with keyboard
- **Screen reader**: Describe canvas content to screen readers
- **High contrast**: Support high contrast mode
- **Zoom support**: Support browser zoom up to 200%

## Security Guidelines

### Client-side Security
- **Input sanitization**: Sanitize all user inputs
- **XSS prevention**: Prevent cross-site scripting attacks
- **CSRF protection**: Implement CSRF protection
- **Content Security Policy**: Implement proper CSP headers

### Authentication Security
- **Token management**: Secure token storage and handling
- **Session management**: Proper session timeout and renewal
- **Route protection**: Protect sensitive routes
- **Permission checking**: Check permissions on client and server

## Monitoring and Analytics

### Performance Monitoring
- **Core Web Vitals**: Monitor LCP, FID, CLS
- **Bundle size**: Track bundle size over time
- **Load times**: Monitor page load times
- **Error rates**: Track JavaScript errors

### User Analytics
- **Feature usage**: Track feature adoption and usage
- **User flows**: Analyze user behavior and flows
- **Conversion rates**: Monitor conversion funnels
- **A/B testing**: Implement A/B testing for features