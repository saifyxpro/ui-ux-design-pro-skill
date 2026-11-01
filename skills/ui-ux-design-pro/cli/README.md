# Design Pro CLI

The "Masterpiece" UI/UX design CLI. Built with **Bun**, **Orama**, and **TypeScript**.

## Features

- **Search**: Fuzzy search across 1,800+ design data points (styles, colors, reasoning).
- **Icons**: Browse and find the best icon libraries.
- **Audit**: Scan your UI code for accessibility and quality issues.
- **Generate**: Create full design systems (tokens, palettes, typography) from a text query.

## Setup

1.  **Install Bun**: [https://bun.sh/](https://bun.sh/)
2.  **Install Dependencies**:
    ```bash
    bun install
    ```

## Usage

You can run the CLI directly with `bun run`:

```bash
# Search
bun run index.ts search "glassmorphism"
bun run index.ts search "glassmorphism" --domain style
bun run index.ts search "useEffect" --stack react

# Icons
bun run index.ts icons "arrow"

# Audit
bun run index.ts audit ../src/App.tsx

# Generate Design System
bun run index.ts generate "fintech dashboard" --stack nextjs --output system.json
```

## Commands

- `search <query>`: Search the design knowledge base, optionally restricted with `--domain` or `--stack`. An unknown domain or stack is an error.
- `icons <query>`: Find icons and icon libraries.
- `audit <files>`: Audit UI files.
- `generate <query>`: Generate a design system. `--stack` adds that framework's guidelines to the output.

**Domains:** `product`, `style`, `typography`, `color`, `landing`, `chart`, `ux`, `reasoning`, `react`, `web`, `icon`, `icon-library`, `component`, `hallucination`.

**Stacks:** the file names in `data/stacks/` (`nextjs`, `react-native`, `html-tailwind`...).
