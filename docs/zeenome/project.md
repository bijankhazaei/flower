# Zeenome Web Frontend Project

## Project Overview
- **Name**: Zeenome Longevity Web Application
- **Type**: B2C Health & Longevity Services Platform
- **Primary Market**: Iran
- **Business Model**: Subscription-based health journey services

Zeenome is a comprehensive longevity platform offering personalized health services through structured "Journeys". Each journey provides specific health insights, reports, and recommendations based on user data, questionnaires, and lab results.

### Journey Types & Dependencies
**Independent Journeys:**
- **Biological Age Journey**: Questionnaire-based biological age calculation (no dependencies)

**Foundation Journeys:**
- **Life Style Score Journey**: Lifestyle assessment across multiple dimensions (sleep, habits, etc.)
- **Longevity Report Journey**: Comprehensive longevity analysis (requires Life Style Score + lab test upload)

**Advanced Journeys** (all require Longevity Report completion):
- **Diet Journey**: Personalized 1-month nutrition plan
- **Sport Program Journey**: Customized 6-month fitness program
- **Intervention Journey**: Weekly lifestyle modification instructions
- **Pill Pack Journey**: Personalized daily supplement regimen (1-month supply)

### Business Model
- **Pricing**: Individual journey pricing with subscription-based access
- **Purchase Limitations**: Advanced cart limitations and dependency validation
- **Duration-based Services**: Varying service periods (1-month to 6-month programs)

## Application Routes
```
app/                          # Next.js App Router
├── (dev)/                    # Development route group (NEVER INVESTIGATE; NEVER ALTER)
│   ├── __design_system/      # Internal design system preview
│   ├── __happy_birthday/     # Special occasion feature
│   └── __test/               # Development testing
├── (public)/                 # Public routes (no authentication required)
│   ├── (landing)/            # Homepage with journey showcase
│   ├── about-us/             # Company information
│   ├── blog/                 # Content marketing
│   │   ├── articles/         # Health articles
│   │   ├── news/             # Company news
│   │   └── webinars/         # Educational content
│   ├── contact-us/           # Contact information
│   └── store/                # Journey catalog and details
├── auth/                     # Authentication system
│   ├── sign-in/              # User login
│   └── sign-out/             # User logout
├── panel/                    # Authenticated user dashboard
│   ├── (dashboard)/          # Main dashboard with journey status
│   ├── basket/               # Shopping cart management
│   ├── orders/               # Purchase history and order tracking
│   └── profile/              # User account management
├── questionnaire/            # Universal questionnaire system
├── report/                   # Journey results and reports
│   ├── BiologicalAgeReport/  # Biological age results
│   ├── LifeStyleScoreReport/ # Lifestyle assessment results
│   ├── LongevityReport/      # Comprehensive longevity analysis
│   ├── DietReport/           # Nutrition plan delivery
│   ├── SportProgramReport/   # Fitness program delivery
│   ├── InterventionReport/   # Lifestyle intervention guidance
│   └── PillPackReport/       # Supplement recommendations
├── error/                    # Error handling pages
└── s/                        # Short URL redirects and sharing
```

## Architecture Pattern
**Modular Monolith** with feature-based organization and clean separation of concerns.

## Technology Stack
- **Framework**: Next.js 15.1.7 with App Router
- **Language**: TypeScript with React 19
- **Styling**: Tailwind CSS + SCSS
- **UI Components**: Radix UI primitives with custom design system
- **State Management**: Jotai (atomic) + Zustand (complex state)
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios with custom API service layer
- **Internationalization**: i18next (English/Persian with RTL support)
- **Date Handling**: Jalali Moment (Persian calendar)
- **Animations**: Framer Motion
- **Development**: Turbopack, ESLint, TypeScript

## Backend Integration
- **API Architecture**: REST API consumption only (no backend operations in Next.js)
- **Authentication**: Token-based (localStorage) for CSR calls
- **SSR Limitations**: Only public/unauthenticated endpoints accessible in SSR
- **Backend Stack**: Laravel + MySQL + RabbitMQ + AI microservices (external)

## Key Features
- **Multi-language Support**: English/Persian with RTL layout
- **Theme System**: Light/Dark mode with automatic switching
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Progressive Enhancement**: SSR for SEO + CSR for interactivity
- **Type Safety**: Full TypeScript coverage with strict validation
- **Accessibility**: WCAG compliant components
- **Performance**: Turbopack for fast development, standalone builds for production

## Development & Deployment
- **Development**: Hot reload with Turbopack
- **Build**: Standalone output for containerization
- **CI/CD**: GitLab CI with Docker multi-stage builds
- **Deployment**: Docker containers with separate dev/production pipelines
- **Code Generation**: Automated API endpoint and middleware generation