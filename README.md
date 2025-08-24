# Porto Architecture Documentation

## Overview

Porto is a modern software architectural pattern designed to help developers build scalable, maintainable, and testable applications. It provides a structured approach to organizing code by separating concerns and establishing clear boundaries between different layers of the application.

## Core Principles

### 1. Separation of Concerns
- Each component has a single, well-defined responsibility
- Business logic is isolated from infrastructure concerns
- Clear boundaries between different layers

### 2. Dependency Inversion
- High-level modules don't depend on low-level modules
- Both depend on abstractions
- Abstractions don't depend on details

### 3. Testability
- Components are easily testable in isolation
- Dependencies can be mocked or stubbed
- Clear interfaces enable unit testing

## Architecture Layers

### Ship Layer (Framework)
```
app/
├── Ship/
│   ├── Engine/
│   ├── Features/
│   ├── Parents/
│   └── Middlewares/
```

### Containers Layer (Modules)
```
app/
├── Containers/
│   ├── User/
│   │   ├── Actions/
│   │   ├── Tasks/
│   │   ├── Models/
│   │   ├── Data/
│   │   ├── UI/
│   │   └── Tests/
│   └── Product/
│       ├── Actions/
│       ├── Tasks/
│       ├── Models/
│       ├── Data/
│       ├── UI/
│       └── Tests/
```

## Component Types

### Actions
- **Purpose**: Orchestrate business operations
- **Responsibility**: Coordinate multiple Tasks
- **Example**: `CreateUserAction`, `ProcessPaymentAction`

```php
class CreateUserAction extends Action
{
    public function run(CreateUserRequest $request): User
    {
        $user = app(CreateUserTask::class)->run($request->toArray());
        app(SendWelcomeEmailTask::class)->run($user);
        
        return $user;
    }
}
```

### Tasks
- **Purpose**: Contain specific business logic
- **Responsibility**: Single business operation
- **Example**: `CreateUserTask`, `ValidateEmailTask`

```php
class CreateUserTask extends Task
{
    public function run(array $data): User
    {
        return app(UserRepository::class)->create($data);
    }
}
```

### Models
- **Purpose**: Represent business entities
- **Responsibility**: Data structure and relationships
- **Example**: `User`, `Product`, `Order`

### Repositories
- **Purpose**: Data access abstraction
- **Responsibility**: Database operations
- **Location**: `Data/Repositories/`

### Transformers
- **Purpose**: Data transformation
- **Responsibility**: Format data for API responses
- **Location**: `UI/API/Transformers/`

### Requests
- **Purpose**: Input validation
- **Responsibility**: Validate and sanitize input
- **Location**: `UI/API/Requests/` or `UI/WEB/Requests/`

### Controllers
- **Purpose**: Handle HTTP requests
- **Responsibility**: Route requests to Actions
- **Location**: `UI/API/Controllers/` or `UI/WEB/Controllers/`

## Container Structure

Each container represents a bounded context and contains:

```
Container/
├── Actions/           # Business operations orchestration
├── Tasks/            # Specific business logic
├── Models/           # Business entities
├── Data/
│   ├── Migrations/   # Database migrations
│   ├── Seeders/      # Database seeders
│   ├── Factories/    # Model factories
│   └── Repositories/ # Data access layer
├── UI/
│   ├── API/
│   │   ├── Controllers/
│   │   ├── Requests/
│   │   ├── Transformers/
│   │   └── Routes/
│   └── WEB/
│       ├── Controllers/
│       ├── Requests/
│       ├── Views/
│       └── Routes/
├── Tests/
│   ├── Unit/
│   └── Functional/
├── Configs/
└── Providers/
```

## Request Flow

1. **Route** → Defines URL endpoints
2. **Controller** → Handles HTTP request
3. **Request** → Validates input data
4. **Action** → Orchestrates business logic
5. **Task** → Executes specific operations
6. **Repository** → Handles data persistence
7. **Transformer** → Formats response data

## Benefits

### Scalability
- Modular structure allows independent scaling
- Clear separation enables team collaboration
- Easy to add new features without affecting existing code

### Maintainability
- Consistent structure across all modules
- Easy to locate and modify specific functionality
- Clear dependencies and relationships

### Testability
- Each component can be tested in isolation
- Mock dependencies easily
- Clear interfaces for unit testing

### Reusability
- Tasks can be reused across different Actions
- Repositories can be shared between containers
- Common functionality in Ship layer

## Best Practices

### Naming Conventions
- Actions: `{Verb}{Entity}Action` (e.g., `CreateUserAction`)
- Tasks: `{Verb}{Entity}Task` (e.g., `FindUserTask`)
- Models: `{Entity}` (e.g., `User`, `Product`)
- Controllers: `{Entity}Controller` (e.g., `UserController`)

### Dependencies
- Actions can call multiple Tasks
- Tasks should be atomic and focused
- Use dependency injection for loose coupling
- Avoid circular dependencies

### Error Handling
- Use custom exceptions for business logic errors
- Handle errors at appropriate levels
- Provide meaningful error messages

### Testing Strategy
- Unit tests for Tasks and Models
- Functional tests for Actions
- Integration tests for Controllers
- Mock external dependencies

## Implementation Guidelines

### 1. Start with Containers
- Identify bounded contexts
- Create container structure
- Define Models and relationships

### 2. Build Data Layer
- Create Repositories
- Implement database migrations
- Add seeders and factories

### 3. Implement Business Logic
- Create Tasks for specific operations
- Build Actions to orchestrate Tasks
- Add validation and error handling

### 4. Add UI Layer
- Create Controllers
- Define Request validation
- Implement Transformers
- Set up Routes

### 5. Write Tests
- Unit tests for core logic
- Functional tests for workflows
- Integration tests for APIs

## Common Patterns

### Repository Pattern
```php
interface UserRepositoryInterface
{
    public function create(array $data): User;
    public function findById(int $id): ?User;
    public function update(int $id, array $data): User;
    public function delete(int $id): bool;
}
```

### Service Provider Pattern
```php
class ContainerServiceProvider extends ServiceProvider
{
    public function register()
    {
        $this->app->bind(
            UserRepositoryInterface::class,
            UserRepository::class
        );
    }
}
```

### Transformer Pattern
```php
class UserTransformer extends Transformer
{
    public function transform(User $user): array
    {
        return [
            'id' => $user->id,
            'name' => $user->name,
            'email' => $user->email,
            'created_at' => $user->created_at->toISOString(),
        ];
    }
}
```

## Conclusion

Porto architecture provides a robust foundation for building scalable applications by enforcing clear separation of concerns, promoting code reusability, and ensuring maintainability. By following its principles and patterns, development teams can create applications that are easier to understand, test, and extend.
