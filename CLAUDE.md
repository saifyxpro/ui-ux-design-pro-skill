

## Project Overview

**UI/UX Design Pro** is a data-driven design intelligence toolkit providing searchable databases of UI styles, color palettes, font pairings, chart types, reasoning rules, and UX guidelines.

**Technical Stack (2026 Shift):**

- **Runtime:** Bun (TypeScript)
- **Search Engine:** Orama (Fuzzy, Stemming, Typed)
- **CLI Framework:** cac
- **Data Source:** CSV Files (Parsed at runtime)

## CLI Commands

All logic is centralized in the `cli/` directory. Use `bun` to execute commands.

```bash
# Full design system generation (Markdown output)
bun run cli/index.ts generate "fintech dashboard" --stack nextjs --output system.md

# Search across all databases (Sub-50ms)
bun run cli/index.ts search "glassmorphism" --domain style

# Audit UI code quality
bun run cli/index.ts audit src/App.tsx

# Icon search
bun run cli/index.ts icons "arrow"
```

**Available domains:** `product`, `style`, `typography`, `color`, `landing`, `chart`, `ux`, `reasoning`, `react`, `web`

**Available stacks (16):** `html-tailwind`, `react`, `nextjs`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `astro`, `angular`, `remix`, `solidjs`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

## Architecture

```text
ui-ux-design-pro-skill/
├── cli/                        # Unified CLI (Bun/TypeScript)
│   ├── index.ts                # Entry point
│   ├── commands/               # Command logic
│   ├── lib/                    # Shared libraries (Orama, generators)
│   └── data/                   # 27 CSV databases (1,875+ rows)
│       ├── styles.csv
│       ├── typography.csv
│       ├── colors.csv
│       ├── stacks/             # 16 framework guides
│       └── ...
├── skills/
│   └── ui-ux-design-pro/       # AI Skill Definitions
│       ├── SKILL.md            # Main prompt instructions
│       └── references/         # 11 design methodology docs
```

## Sync Rules

**Source of Truth:**

1. **Code/Logic:** `cli/` directory.
2. **Data:** `cli/data/` directory.
3. **Prompt/Skill:** `skills/ui-ux-design-pro/SKILL.md`.

## Prerequisites

- **Bun 1.0+** (Required)
- Node.js 18+ (Optional)

## Git Workflow

1. Create feature branch: `git checkout -b feat/my-feature`
2. Commit changes
3. Push branch
4. Create PR
