# Kintsu Design Guidelines

## Design Approach
**Reference-Based**: Draw inspiration from premium SaaS platforms (Linear, Stripe) combined with kintsugi-inspired artisanal craftsmanship. Balance minimalist precision with warm, restorative visual language.

## Brand Identity

**Positioning**: The Restorative Craftsman archetype - transforming career setbacks into refined strengths  
**Taglines**: 
- Primary: "Polish Your Career Path"
- Secondary: "Rebuild. Refine. Rise."

**Core Visual Metaphor**: Kintsugi pottery repair - celebrate breaks filled with gold, creating stronger, more beautiful results

## Color Palette

- **Indigo (Primary)**: #0B1B3A - Deep, professional base
- **Warm Gold (Accent)**: #C5A95A - Kintsugi seam highlights
- **Soft Sand (Background)**: #FAF7F2 - Warm, inviting canvas
- **Graphite (Text)**: #1F2937 - High readability
- **Muted Gray (UI)**: #9CA3AF - Secondary elements

**Dark Mode**: Slightly lighter gold (#D4BC7A) on dark backgrounds for visibility

## Typography

**Font Families**: Inter or Poppins for headings, Inter or Roboto for body  
**Hierarchy**:
- H1: 600-800 weight, bold, slightly condensed
- Body: 16px base mobile, 400-500 weight, 1.6 line-height
- Small/UI: 14px / 0.875rem

**Style**: Left-aligned headings on large screens, generous spacing for readability

## Layout System

**Spacing Units**: Tailwind units of 4, 6, 8, 12, 16, 20, 24, 32 for consistent rhythm  
**Containers**: max-w-7xl for full sections, max-w-6xl for content, max-w-prose for text  
**Vertical Rhythm**: py-12 mobile, py-20 desktop for section padding

## Visual Style

**Aesthetic**: Minimalist premium with tactile warmth  
**Key Elements**:
- Thin gold lines as section separators (mimicking kintsugi seams)
- Soft glass panels for CTA cards (subtle backdrop-blur)
- Duotone overlays (indigo + gold) for hero images
- Editorial photography: diverse professionals + close-up kintsugi pottery textures

**Motion**: Subtle scale + fade on CTAs (80-150ms), respect prefers-reduced-motion

## Page Sections & Components

### Home Page
1. **Hero**: Headline "Transform your career setbacks into golden opportunities" + sub-headline + dual CTAs (Start 14-Day Trial + View Pricing) + kintsugi hero image
2. **Trust Pillars**: 3-icon block (AI tailoring, Privacy-first, Real outcomes)
3. **Features**: 3-4 cards with pillars (Repair with Precision, Learn & Level Up, Trusted Results)
4. **Pricing Preview**: Tier cards with CTA to full pricing
5. **Testimonials**: Carousel with headshots, roles, companies
6. **Footer**: Newsletter signup, navigation, social links

### Pricing Page
- Three-tier comparison table (Starter, Professional, Executive)
- Annual/monthly toggle
- Clear feature bullets with kintsugi-themed language
- "Begin your golden repair" type CTAs

### Employers Page
- Benefits section with customer logos
- Job posting form: company name, role, location (remote toggle), salary range, description (textarea), contact email, website, logo upload
- Pricing for employers
- Submit via mailto fallback with webhook placeholder

### Jobs Page
- Public board with client-side filtering (role, location, tags)
- Job cards with key info
- Static jobs.json data source

### About Page
- Kintsugi philosophy story with close-up pottery image
- Team section with mission
- Gold seam running horizontally through background

## Component Library

**Navigation**: Logo left, links center/right, CTA button, mobile hamburger  
**Buttons**: Primary (gold), Secondary (outlined), with subtle hover scale  
**Cards**: Soft shadows, rounded corners (8-12px), glass effect for CTAs  
**Forms**: Visible labels, honeypot spam protection, accessible validation  
**Modals**: Contact form, job posting, centered with backdrop  
**Chat Widget**: Floating bottom-right gold circle with icon  
**Dark Mode Toggle**: Sun/moon icon, top-right header

## Accessibility

- WCAG AA contrast minimum, AAA for hero text
- Gold outline (2px) for keyboard focus states
- ARIA labels for navigation, forms, live regions
- Semantic HTML throughout
- All interactive elements keyboard-accessible

## Images

**Hero Section**: Large full-width image featuring either:
- Close-up of kintsugi pottery with visible gold seams OR
- Diverse professional with duotone indigo/gold overlay
- Ensure buttons on images have blurred backgrounds (backdrop-blur-sm)

**Supporting Images**:
- Feature sections: Editorial portraits of professionals
- About page: Detailed kintsugi pottery texture
- Testimonials: Customer headshots (circular crops)
- All images optimized WebP format, lazy-loaded

## Messaging Guidelines

**AI Positioning**: "AI-powered" for capabilities, "AI-assisted" for human-equivalent claims  
**Honesty**: Add footnotes "based on internal benchmarks" for numeric claims  
**Tone**: Professional yet warm, restorative not desperate, precise not hyped

## Technical Notes

- SEO: Open Graph, Twitter cards, canonical links
- Performance: Optimized images, preconnect to fonts
- Analytics placeholder for Google Analytics/Matomo
- Sitemap.xml and robots.txt included