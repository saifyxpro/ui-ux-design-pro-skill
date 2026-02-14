## When to Apply

Reference these guidelines when:
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements
- Running design system generation
- Auditing UI code quality

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Accessibility | CRITICAL | `ux` |
| 2 | Touch & Interaction | CRITICAL | `ux` |
| 3 | Performance | HIGH | `ux` |
| 4 | Layout & Responsive | HIGH | `ux` |
| 5 | Typography & Color | MEDIUM | `typography`, `color` |
| 6 | Animation | MEDIUM | `ux` |
| 7 | Style Selection | MEDIUM | `style`, `product` |
| 8 | Charts & Data | LOW | `chart` |
| 9 | Design Tokens | MEDIUM | `tokens` |
| 10 | Contrast & WCAG | CRITICAL | `contrast` |

## Quick Reference

### 1. Accessibility (CRITICAL)

- `color-contrast` - Minimum 4.5:1 ratio (WCAG AA), 7:1 for AAA
- `focus-states` - Visible focus rings on all interactive elements
- `alt-text` - Descriptive alt text for meaningful images
- `aria-labels` - aria-label for icon-only buttons
- `keyboard-nav` - Tab order matches visual order
- `form-labels` - Use label with for attribute
- `prefers-reduced-motion` - Respect motion preferences
- `screen-reader` - Semantic HTML + ARIA landmarks

### 2. Touch & Interaction (CRITICAL)

- `touch-target-size` - Minimum 44x44px touch targets (48x48px recommended)
- `hover-vs-tap` - Use click/tap for primary interactions
- `loading-buttons` - Disable button during async operations
- `error-feedback` - Clear error messages near problem
- `cursor-pointer` - Add cursor-pointer to all clickable elements
- `haptic-feedback` - Consider vibration on mobile interactions

### 3. Performance (HIGH)

- `image-optimization` - Use WebP/AVIF, srcset, lazy loading
- `reduced-motion` - Check prefers-reduced-motion
- `content-jumping` - Reserve space for async content (skeleton screens)
- `code-splitting` - Lazy load routes and heavy components
- `font-loading` - Use font-display: swap with preload

### 4. Layout & Responsive (HIGH)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - Minimum 16px body text on mobile
- `horizontal-scroll` - Ensure content fits viewport width
- `z-index-management` - Define z-index scale (10, 20, 30, 50)
- `container-queries` - Use container queries for component-level responsiveness
- `fluid-typography` - Use clamp() for responsive font sizes

### 5. Typography & Color (MEDIUM)

- `line-height` - Use 1.5-1.75 for body text
- `line-length` - Limit to 65-75 characters per line
- `font-pairing` - Match heading/body font personalities
- `color-system` - Use oklch() for perceptually uniform color scales
- `design-tokens` - Use CSS custom properties for all values

### 6. Animation (MEDIUM)

- `duration-timing` - Use 150-300ms for micro-interactions
- `transform-performance` - Use transform/opacity, not width/height
- `loading-states` - Skeleton screens or spinners
- `easing-functions` - Use cubic-bezier for natural motion
- `stagger-animations` - Stagger list item animations (50ms delay)

### 7. Style Selection (MEDIUM)

- `style-match` - Match style to product type and industry
- `consistency` - Use same style across all pages
- `no-emoji-icons` - Use SVG icons (Heroicons, Lucide, Phosphor)
- `design-system` - Generate tokens before coding

### 8. Charts & Data (LOW)

- `chart-type` - Match chart type to data type
- `color-guidance` - Use accessible color palettes (colorblind-safe)
- `data-table` - Provide table alternative for accessibility
- `responsive-charts` - Charts adapt to container width

### 9. Design Tokens (MEDIUM)

- `token-presets` - Use industry presets (fintech, healthcare, etc.)
- `css-variables` - Generate with `generate_tokens.py`
- `type-scale` - Calculate with `generate_typography.py`
- `color-harmony` - Generate with `generate_palette.py`

### 10. Contrast & WCAG (CRITICAL)

- `wcag-aa` - 4.5:1 for normal text, 3:1 for large text
- `wcag-aaa` - 7:1 for normal text, 4.5:1 for large text
- `apca` - Lc 60+ for body text, Lc 75+ for small text
- `check-tool` - Validate with `check_contrast.py`

## How to Use

Search specific domains using the CLI tool below.

---


