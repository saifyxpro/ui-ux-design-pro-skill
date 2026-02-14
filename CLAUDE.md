# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UI/UX Design Pro is a data-driven design intelligence toolkit providing searchable databases of UI styles, color palettes, font pairings, chart types, reasoning rules, and UX guidelines. It works as a skill/workflow for AI coding assistants (Claude Code, Cursor, Windsurf, Antigravity, and 14 more).

## CLI Commands

All scripts are accessible via the unified CLI:

```bash
# Full design system generation
python3 src/ui-ux-design-pro/scripts/design_cli.py system "<query>" [--stack <stack>] [--output file.json]

# BM25 search across all databases
python3 src/ui-ux-design-pro/scripts/design_cli.py search "<query>" --domain <domain>

# WCAG/APCA contrast checker
python3 src/ui-ux-design-pro/scripts/design_cli.py contrast "#1E293B" "#F8FAFC" --level AAA

# Color harmony palette generator
python3 src/ui-ux-design-pro/scripts/design_cli.py palette "#2563EB" --harmony triadic --count 5

# CSS design token generator
python3 src/ui-ux-design-pro/scripts/design_cli.py tokens --preset fintech --format css

# Modular type scale calculator
python3 src/ui-ux-design-pro/scripts/design_cli.py typography --scale golden --format css

# UI code quality auditor
python3 src/ui-ux-design-pro/scripts/design_cli.py audit ./src/App.tsx
```

**Available domains:** `product`, `style`, `typography`, `color`, `landing`, `chart`, `ux`, `reasoning`, `react`, `web`, `prompt`

**Available stacks (16):** `html-tailwind` (default), `react`, `nextjs`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `astro`, `angular`, `remix`, `solidjs`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

## Architecture

```
src/ui-ux-design-pro/                # Source of Truth
├── SKILL.md                         # Main skill document
├── data/                            # 27 CSV databases (1,875+ rows)
│   ├── styles.csv, typography.csv, charts.csv, ...
│   └── stacks/                      # 16 stack-specific guidelines
├── references/                      # 11 design methodology docs
├── scripts/                         # 8 Python scripts
│   ├── design_cli.py                # Unified CLI entry point
│   ├── search_design.py             # BM25 search engine
│   ├── generate_system.py           # Design system generator
│   ├── generate_tokens.py           # CSS token generator (8 presets)
│   ├── generate_palette.py          # Color harmony generator (6 modes)
│   ├── generate_typography.py       # Type scale calculator (8 ratios)
│   ├── check_contrast.py            # WCAG/APCA contrast checker
│   └── audit_ui.py                  # UI code auditor (12 rules)
└── templates/                       # 18 platform templates
    ├── base/                        # Base templates with placeholders
    └── platforms/                   # Platform-specific JSON configs

.claude/skills/ui-ux-design-pro/     # Claude Code skill (symlinks to src/)
.claude-plugin/                      # Claude Marketplace publishing
```

## Sync Rules

**Source of Truth:** `src/ui-ux-design-pro/`

When modifying files:

1. **Data & Scripts** — Edit in `src/ui-ux-design-pro/`:
   - `data/*.csv` and `data/stacks/*.csv`
   - `scripts/*.py`
   - Changes automatically available via symlinks in `.claude/`

2. **Templates** — Edit in `src/ui-ux-design-pro/templates/`:
   - `base/skill-content.md` — Common SKILL.md content
   - `base/quick-reference.md` — Quick reference section
   - `platforms/*.json` — Platform-specific configs

3. **SKILL.md** — Copy from `src/` to `.claude/skills/` after changes:
   ```bash
   cp src/ui-ux-design-pro/SKILL.md .claude/skills/ui-ux-design-pro/SKILL.md
   ```

## Prerequisites

Python 3.x (no external dependencies required)

## Git Workflow

Never push directly to `main`. Always:

1. Create a new branch: `git checkout -b feat/...` or `fix/...`
2. Commit changes
3. Push branch: `git push -u origin <branch>`
4. Create PR: `gh pr create`
