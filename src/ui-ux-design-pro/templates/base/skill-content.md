# {{TITLE}}

{{DESCRIPTION}}
{{QUICK_REFERENCE}}
## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## How to Use This {{SKILL_OR_WORKFLOW}}

When user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, Angular, Remix, SolidJS, or default to `html-tailwind`

### Step 2: Generate Design System (REQUIRED)

**Always start with the design system generator** to get comprehensive recommendations with reasoning:

```bash
python3 {{SCRIPT_DIR}}/design_cli.py system "<product_type> <industry> <keywords>" [--stack <stack>] [--output design.json]
```

This command:
1. Searches 11 domains in parallel using BM25 ranking
2. Applies 131 reasoning rules from `ui-reasoning.csv` to select best matches
3. Returns complete design system: pattern, style, colors, typography, effects
4. Generates 83 CSS design tokens
5. Includes anti-patterns to avoid

**Example:**
```bash
python3 {{SCRIPT_DIR}}/design_cli.py system "beauty spa wellness service elegant" --stack nextjs
```

### Step 2b: Supplement with Individual Tools

After the design system, use specialized tools for deeper analysis:

```bash
# BM25 search across all 27 CSV databases
python3 {{SCRIPT_DIR}}/design_cli.py search "<keywords>" --domain <domain>

# Check color contrast (WCAG 2.2 + APCA)
python3 {{SCRIPT_DIR}}/design_cli.py contrast "#1E293B" "#F8FAFC" --level AAA

# Generate color harmony palette
python3 {{SCRIPT_DIR}}/design_cli.py palette "#2563EB" --harmony triadic --count 5

# Generate CSS design tokens with industry presets
python3 {{SCRIPT_DIR}}/design_cli.py tokens --preset fintech --format css

# Calculate modular type scale
python3 {{SCRIPT_DIR}}/design_cli.py typography --scale golden --format css

# Audit UI code quality (12 rules)
python3 {{SCRIPT_DIR}}/design_cli.py audit ./src/App.tsx
```

### Step 2c: Persist Design System (Master + Overrides Pattern)

To save the design system for hierarchical retrieval across sessions:

```bash
python3 {{SCRIPT_DIR}}/design_cli.py system "<query>" --output design-system/MASTER.json
```

This creates:
- `design-system/MASTER.json` — Global Source of Truth with all design rules

**How hierarchical retrieval works:**
1. When building a specific page (e.g., "Checkout"), first check `design-system/pages/checkout.json`
2. If the page file exists, its rules **override** the Master file
3. If not, use `design-system/MASTER.json` exclusively

### Step 3: Stack Guidelines (Default: html-tailwind)

Get implementation-specific best practices. If user doesn't specify a stack, **default to `html-tailwind`**.

```bash
python3 {{SCRIPT_DIR}}/design_cli.py search "<keyword>" --domain stack --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `astro`, `angular`, `remix`, `solidjs`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by industry | saas, ecommerce, healthcare, beauty, fintech |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `reasoning` | Industry design rules | fintech, healthcare, crypto, AI products |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender |
| `web` | Web interface guidelines | aria, focus, keyboard, semantic, virtualize |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Available Stacks (16)

| Stack | Focus |
|-------|-------|
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `nuxtjs` | Nuxt 3, auto-imports, composables |
| `nuxt-ui` | Nuxt UI components, theming |
| `svelte` | Runes, stores, SvelteKit |
| `astro` | Islands, content collections, SSG |
| `angular` | Signals, standalone components, routing |
| `remix` | Loaders, actions, progressive enhancement |
| `solidjs` | Signals, stores, reactive primitives |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | shadcn/ui components, theming, forms |
| `jetpack-compose` | Composables, Modifiers, State Hoisting |

### Token Presets (8)

| Preset | Primary Color | Font | Border Radius |
|--------|---------------|------|---------------|
| `fintech` | #2563EB | Inter | 8px |
| `healthcare` | #059669 | Source Sans Pro | 12px |
| `ecommerce` | #DC2626 | Poppins | 8px |
| `saas` | #7C3AED | Inter | 12px |
| `education` | #2563EB | Nunito | 16px |
| `gaming` | #EF4444 | Orbitron | 4px |
| `luxury` | #1E293B | Playfair Display | 0px |
| `startup` | #8B5CF6 | DM Sans | 12px |

---

## Example Workflow

**User request:** "Build a fintech banking dashboard with dark theme"

### Step 1: Analyze Requirements
- Product type: Fintech/Banking
- Style keywords: dark, professional, data-dense
- Industry: Finance
- Stack: nextjs (or html-tailwind default)

### Step 2: Generate Design System (REQUIRED)

```bash
python3 {{SCRIPT_DIR}}/design_cli.py system "fintech banking dashboard dark professional" --stack nextjs
```

### Step 2b: Supplement with Detailed Searches

```bash
# Check contrast for dark theme colors
python3 {{SCRIPT_DIR}}/design_cli.py contrast "#0F172A" "#F8FAFC" --level AAA

# Generate professional font type scale
python3 {{SCRIPT_DIR}}/design_cli.py typography --scale major-third --format css

# Generate fintech tokens
python3 {{SCRIPT_DIR}}/design_cli.py tokens --preset fintech --format css

# Search for dashboard chart recommendations
python3 {{SCRIPT_DIR}}/design_cli.py search "financial dashboard real-time" --domain chart
```

### Step 3: Stack Guidelines

```bash
python3 {{SCRIPT_DIR}}/design_cli.py search "server components data fetching" --domain stack --stack nextjs
```

**Then:** Synthesize design system + detailed searches and implement the design.

---

## Color Harmony Modes

| Mode | Description | Degrees |
|------|-------------|---------|
| Complementary | Opposite on color wheel | +180° |
| Analogous | Adjacent colors | ±30° |
| Triadic | Three evenly spaced | +120°, +240° |
| Tetradic | Four evenly spaced | +90°, +180°, +270° |
| Split-Complementary | Modified complementary | +150°, +210° |
| Monochromatic | Same hue, varying lightness | — |

## Type Scale Ratios

| Ratio | Value | Feel |
|-------|-------|------|
| Minor Second | 1.067 | Subtle, tight |
| Major Second | 1.125 | Balanced |
| Minor Third | 1.200 | Clean |
| Major Third | 1.250 | Standard (default) |
| Perfect Fourth | 1.333 | Bold |
| Augmented Fourth | 1.414 | Dramatic |
| Perfect Fifth | 1.500 | Very bold |
| Golden | 1.618 | Maximum contrast |

---

## Common Rules for Professional UI

These are frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule | Do | Don't |
|------|----|----- |
| **No emoji icons** | Use SVG icons (Heroicons, Lucide, Phosphor) | Use emojis like 🎨 🚀 ⚙️ as UI icons |
| **Stable hover states** | Use color/opacity transitions on hover | Use scale transforms that shift layout |
| **Correct brand logos** | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes randomly |

### Interaction & Cursor

| Rule | Do | Don't |
|------|----|----- |
| **Cursor pointer** | Add `cursor-pointer` to all clickable elements | Leave default cursor on interactive elements |
| **Hover feedback** | Provide visual feedback (color, shadow, border) | No indication element is interactive |
| **Smooth transitions** | Use `transition-colors duration-200` | Instant state changes or too slow (>500ms) |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----- |
| **Glass card light mode** | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent) |
| **Text contrast light** | Use `#0F172A` (slate-900) for text | Use `#94A3B8` (slate-400) for body text |
| **Muted text light** | Use `#475569` (slate-600) minimum | Use gray-400 or lighter |
| **Border visibility** | Use `border-gray-200` in light mode | Use `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Don't |
|------|----|----- |
| **Floating navbar** | Add `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| **Content padding** | Account for fixed navbar height | Let content hide behind fixed elements |
| **Consistent max-width** | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

---

## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide/Phosphor)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Design tokens used consistently (CSS custom properties)

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation
- [ ] Loading states implemented (skeleton/spinner)

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery
- [ ] Contrast verified with `check_contrast.py`

### Layout
- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile
- [ ] Container queries for component responsiveness

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
- [ ] Semantic HTML landmarks used
- [ ] Validated with `audit_ui.py`

### Design Tokens
- [ ] CSS custom properties for all colors
- [ ] Type scale follows consistent ratio
- [ ] Spacing uses 4px/8px grid
- [ ] Shadows defined in token system
- [ ] Animation durations in tokens


