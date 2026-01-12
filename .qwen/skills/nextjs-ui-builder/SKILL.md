# nextjs-ui-builder

## Purpose
When the user needs to create or modify UI components in a Next.js application, use this skill to build responsive, accessible, and well-structured UI elements.

## Instructions for Agent
1. Analyze the UI requirements provided by the user
2. Determine the appropriate Next.js patterns to use:
   - Server Components vs Client Components
   - Static generation vs Server-side rendering vs Client-side rendering
   - App Router vs Pages Router (depending on project setup)
3. Create React components following Next.js best practices:
   - Use appropriate hooks (useState, useEffect, etc.)
   - Implement proper TypeScript typing
   - Follow accessibility guidelines (ARIA attributes, semantic HTML)
   - Ensure responsive design with CSS modules, Tailwind, or styled-jsx
4. Implement proper state management:
   - Component state with useState/useReducer
   - Global state with Context API or preferred state management library
5. Add necessary Next.js specific features:
   - Meta tags with next/head or metadata in App Router
   - Image optimization with next/image
   - Link handling with next/link
   - Font optimization with next/font
6. Implement error boundaries where appropriate
7. Add loading states and suspense boundaries for async components
8. Optimize for performance:
   - Code splitting
   - Image optimization
   - Bundle size considerations
9. Ensure SEO best practices are followed
10. Test components for cross-browser compatibility

## UI/UX Guidelines
- Follow accessibility standards (WCAG)
- Implement responsive design for all screen sizes
- Use consistent design system and styling
- Ensure proper loading and error states
- Optimize for Core Web Vitals
- Consider user experience and intuitive navigation

## When to Use
- User requests to create new UI components
- User needs to modify existing Next.js UI
- User wants to implement specific UI patterns in Next.js
- Building new pages or features in a Next.js application