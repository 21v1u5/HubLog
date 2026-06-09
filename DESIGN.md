---
name: Modern Technical Academic
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#c4c5d9'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#8e90a2'
  outline-variant: '#434656'
  surface-tint: '#b8c3ff'
  primary: '#b8c3ff'
  on-primary: '#002387'
  primary-container: '#2d5bff'
  on-primary-container: '#efefff'
  inverse-primary: '#104af0'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#00dbe7'
  on-tertiary: '#00363a'
  tertiary-container: '#007980'
  on-tertiary-container: '#c0faff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c3ff'
  on-primary-fixed: '#001355'
  on-primary-fixed-variant: '#0035bd'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#74f5ff'
  tertiary-fixed-dim: '#00dbe7'
  on-tertiary-fixed: '#002022'
  on-tertiary-fixed-variant: '#004f54'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  code:
    fontFamily: geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1200px
  gutter: 24px
---

## Brand & Style
This design system is engineered for high-stakes academic presentations in the technology sector. It merges the rigorous structure of scientific discourse with the sleek, high-performance aesthetic of modern SaaS platforms. The brand personality is authoritative, futuristic, and intellectually precise.

The visual style is **Modern Minimalist with subtle Glassmorphism**. It prioritizes extreme clarity and information hierarchy, ensuring that complex data remains the focal point while being housed in a sophisticated, dark-themed environment. The goal is to evoke a sense of "The Future of Research"—clean, focused, and technologically advanced.

## Colors
The palette is rooted in a "Deep Graphite" foundation to provide a restful, high-contrast environment for long-form technical reading.

- **Primary (Electric Blue):** Used for primary actions, data highlights, and essential navigational cues.
- **Secondary (Soft Neon Purple):** Reserved for accenting complex diagrams or secondary data sets to provide visual depth without causing fatigue.
- **Neutral Stack:** A range of deep greys (#0D0D0D to #1A1A1A) creates the "SaaS" surface feel, using subtle shifts in value to indicate hierarchy rather than heavy lines.
- **Status Colors:** Use Tertiary (Cyan) for success/innovation metrics and a muted coral for warnings or critical data points.

## Typography
The typography system utilizes **Geist** for its technical, developer-centric precision in headlines and labels, paired with **Inter** for body text to ensure maximum legibility during presentations.

- **Headlines:** Should be used sparingly to anchor sections. Use heavy weights (600-700) against the dark background to ensure readability from a distance.
- **Body Text:** Maintain a line height of 1.5x to 1.6x. This "breathability" is crucial for academic content which can often feel dense.
- **Labels:** Use uppercase Geist for metadata, figure captions, and small UI labels to create a distinct "instrumentation" feel.

## Layout & Spacing
The layout follows a **12-column fixed grid** model optimized for 16:9 presentation ratios. 

- **Whitespace:** Use the `xl` (64px) spacing unit for margins between major content blocks. This design system relies on "generous breathing room" to signify premium quality.
- **Alignment:** All elements must strictly adhere to the grid. Use left-aligned text for readability in technical contexts.
- **Reflow:** For mobile views of the presentation (e.g., handouts), the 12-column grid collapses to a single column, with padding reducing from `lg` to `md`.

## Elevation & Depth
Depth is achieved through **Tonal Layering** and **Subtle Glassmorphism** rather than traditional heavy shadows.

- **Surfaces:** The base background is `#0D0D0D`. Secondary surfaces (cards, sidebars) use `#1A1A1A`.
- **Borders:** Instead of shadows, use 1px borders with a low-opacity white (e.g., `rgba(255, 255, 255, 0.08)`) or a faint tint of the primary color.
- **Backdrop Blur:** For floating elements or modals, use a 12px-20px backdrop blur with a semi-transparent fill (`rgba(26, 26, 26, 0.7)`) to create a "frosted glass" effect that keeps the background visible but non-distracting.
- **Glows:** For high-priority data points, apply a very soft, diffused outer glow using the primary color at 10% opacity.

## Shapes
The shape language is "Softly Geometric." 

- **Standard Radius:** 0.5rem (8px) for cards and main containers. This balances the "hard" technical nature of the content with a modern, approachable feel.
- **Large Radius:** 1rem (16px) for major sections or hero cards.
- **Interactive Elements:** Buttons and tags should utilize the standard radius to maintain consistency across the UI.

## Components
- **Cards:** Use the `#1A1A1A` surface with a 1px `white/0.08` border. Apply a subtle internal padding of `md` (24px).
- **Buttons:** 
  - *Primary:* Solid Electric Blue with white text.
  - *Secondary:* Ghost style with 1px Electric Blue border and text.
- **Chips/Tags:** Small, semi-transparent backgrounds with Geist labels. Use for categorizing technical stacks or research tags.
- **Lists:** Use linear icons (2px stroke width) as bullets. Maintain high vertical spacing between items.
- **Input Fields:** Darker than the surface background (`#080808`) with a 1px border that glows Primary Blue on focus.
- **Data Visuals:** Charts should use the Electric Blue, Purple, and Cyan palette. Grid lines in charts should be extremely faint (`white/0.05`).
- **Icons:** Use thin-stroke, linear icons. Avoid filled icons to maintain the minimalist, airy aesthetic.