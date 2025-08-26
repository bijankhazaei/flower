# Zeenome Design System Rules

## Color Palette & Schema System

### Approved Color Palette
**ONLY use these colors - no colors outside this palette are allowed:**

- **gray**: Shades 50-950 (50 closest to current schema)
- **dominant**: Primary brand color, shades 100-900 (100 closest to current schema)
- **complement**: Success color, shades 100-900 (100 closest to current schema)
- **error**: Error/danger color, shades 100-900 (100 closest to current schema)
- **information**: Info color, shades 100-900 (100 closest to current schema)
- **warning**: Warning color, shades 100-900 (100 closest to current schema)

### Color Usage Examples
```css
/* Background colors */
.bg-gray-50 .bg-gray-950        /* Neutral backgrounds */
.bg-dominant-100 .bg-dominant-900  /* Brand backgrounds */
.bg-complement-200              /* Success states */
.bg-error-100                   /* Error backgrounds */
.bg-information-200             /* Info backgrounds */
.bg-warning-100                 /* Warning backgrounds */

/* Text colors */
.text-gray-900 .text-gray-100   /* Body text */
.text-dominant-600              /* Brand text */
.text-error-700                 /* Error text */
```

### Schema Classes
```css
/* Schema-specific styling */
.light:bg-dominant-100  /* Light mode only */
.dark:bg-dominant-800   /* Dark mode only */

/* Direction-specific styling */
.ltr:text-left         /* Left-to-right only */
.rtl:text-right        /* Right-to-left only */
```

### Schema Management
- **Hook**: `useSchema()` from `schemaService`
- **Values**: `'light' | 'dark'`
- **Auto-detection**: System preference with manual override

## Tailwind CSS Guidelines

### Directional Classes (RTL/LTR Support)
**NEVER use left/right classes directly. Always use logical properties:**

```css
/* ❌ WRONG - Never use these */
.ml-4, .mr-4, .pl-2, .pr-2
.left-0, .right-0
.border-l, .border-r

/* ✅ CORRECT - Always use these */
.ms-4, .me-4, .ps-2, .pe-2    /* margin/padding start/end */
.start-0, .end-0               /* positioning start/end */
.border-s, .border-e           /* border start/end */
```

### Responsive Design
```css
/* Mobile-first approach */
.text-sm md:text-base lg:text-lg
.flex-col md:flex-row
.p-4 md:p-6 lg:p-8
```

### Schema & Direction Combinations
```css
/* Complex conditional styling */
.light:ltr:bg-gray-50 .dark:ltr:bg-gray-900
.light:rtl:bg-gray-100 .dark:rtl:bg-gray-800
.light:text-dominant-900 .dark:text-dominant-100
```

## Kit Components System

### Component Resolution
**NEVER import kit components directly. Always use Resolver:**

```tsx
// ❌ WRONG - Never import directly
import { Button } from "@/components/kit/Button";

// ✅ CORRECT - Always use Resolver
import { Resolver } from "@/modules/resolver/Resolver";

const MyComponent = () => (
  <Resolver.Button variant="dominant">
    Click me
  </Resolver.Button>
);
```

### Available Kit Components
- **Form Elements**: `Button`, `Input`, `Select`, `Checkbox`, `Radio`, `Switch`
- **Layout**: `Card`, `Grid`, `Stack`, `Divider`, `Spacer`
- **Navigation**: `Tabs`, `Breadcrumb`, `Pagination`
- **Feedback**: `Alert`, `Badge`, `Progress`, `Skeleton`
- **Overlay**: `Modal`, `Popover`, `Tooltip`, `Drawer`
- **Data Display**: `Table`, `List`, `Avatar`, `Image`

### Component Variants
```tsx
// Button variants
<Resolver.Button variant="dominant" />    // Primary action
<Resolver.Button variant="secondary" />   // Secondary action
<Resolver.Button variant="ghost" />       // Minimal styling
<Resolver.Button variant="destructive" /> // Danger actions

// Size variants
<Resolver.Button size="sm" />
<Resolver.Button size="md" />  // default
<Resolver.Button size="lg" />
```

## Animation System (Framer Motion)

### Basic Animations
```tsx
import { motion } from "framer-motion";

// Fade in/out
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  exit={{ opacity: 0 }}
>

// Slide animations
<motion.div
  initial={{ x: -20, opacity: 0 }}
  animate={{ x: 0, opacity: 1 }}
  transition={{ duration: 0.3 }}
>

// Scale animations
<motion.div
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
```

### Page Transitions
```tsx
// Layout animations
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.4, ease: "easeOut" }}
>
```

### Stagger Animations
```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.div variants={container} initial="hidden" animate="show">
  {items.map(item => (
    <motion.div key={item.id} variants={item}>
      {item.content}
    </motion.div>
  ))}
</motion.div>
```

## Swiper Integration

### Wizard/Step Components
```tsx
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';

// Questionnaire steps
<Swiper
  modules={[Navigation, Pagination]}
  spaceBetween={20}
  slidesPerView={1}
  navigation
  pagination={{ clickable: true }}
  className="questionnaire-swiper"
>
  {steps.map((step, index) => (
    <SwiperSlide key={index}>
      <QuestionnaireStep step={step} />
    </SwiperSlide>
  ))}
</Swiper>
```

### Journey Cards Carousel
```tsx
// Journey showcase
<Swiper
  modules={[Navigation]}
  spaceBetween={16}
  slidesPerView="auto"
  navigation
  breakpoints={{
    640: { slidesPerView: 2 },
    768: { slidesPerView: 3 },
    1024: { slidesPerView: 4 }
  }}
>
  {journeys.map(journey => (
    <SwiperSlide key={journey.id}>
      <JourneyCard journey={journey} />
    </SwiperSlide>
  ))}
</Swiper>
```

### RTL Support for Swiper
```tsx
// Automatic RTL detection
const { isRTL } = useLanguage();

<Swiper
  dir={isRTL ? 'rtl' : 'ltr'}
  modules={[Navigation]}
  // ... other props
>
```

## Layout Patterns

### Container Patterns
```tsx
// Page container
<div className="container mx-auto px-4 md:px-6 lg:px-8">

// Section spacing
<section className="py-12 md:py-16 lg:py-20">

// Card layouts
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

### Flex Patterns
```tsx
// Center content
<div className="flex items-center justify-center min-h-screen">

// Space between
<div className="flex items-center justify-between">

// RTL-safe flex
<div className="flex items-center gap-4">  // Use gap instead of margins
```

## Typography System

### Text Scales
```css
.text-xs     /* 12px */
.text-sm     /* 14px */
.text-base   /* 16px - body text */
.text-lg     /* 18px */
.text-xl     /* 20px */
.text-2xl    /* 24px - headings */
.text-3xl    /* 30px */
.text-4xl    /* 36px */
```

### Font Weights
```css
.font-light    /* 300 */
.font-normal   /* 400 - body text */
.font-medium   /* 500 */
.font-semibold /* 600 - headings */
.font-bold     /* 700 */
```

### RTL Typography
```tsx
// Persian text styling
<p className="font-medium text-base leading-relaxed rtl:font-normal">
  {t('content.description')}
</p>
```

## Component Composition Rules

### Reusable UI Components (`src/components/ui/`)
- Can be imported directly anywhere
- Should use kit components via Resolver
- Must support both schemas and directions
- Should include proper TypeScript interfaces

### Kit Component Guidelines
- Never imported directly
- Must follow strict type definitions in `src/contracts/ui/`
- Implementation based on Radix UI + ShadCN
- All styling via Tailwind classes
- Must support schema and direction variants

### Animation Guidelines
- Use Framer Motion for all animations
- Keep animations subtle and purposeful
- Respect user's motion preferences
- Use consistent timing (0.2s-0.4s for most transitions)
- Implement proper exit animations for route changes

### Swiper Guidelines
- Use for multi-step processes (questionnaires, onboarding)
- Implement proper RTL support
- Include navigation and pagination when needed
- Optimize for touch devices
- Use breakpoints for responsive behavior