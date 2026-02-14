# Component Patterns

## Buttons

### Sizing

```css
--button-height-sm: 28px; /* inline actions, compact UI */
--button-height-md: 36px; /* standard */
--button-height-lg: 44px; /* primary CTA, mobile */

--button-padding-sm: 4px 10px;
--button-padding-md: 8px 16px;
--button-padding-lg: 10px 20px;
```

### Variants

**Primary:** Solid background. One per visible area. Use for the primary action.
**Secondary:** Border or subtle background. Supporting actions.
**Ghost:** No border or background. Inline actions, icon buttons.
**Destructive:** Red/destructive color. Requires confirmation for irreversible actions.

### States

```css
.button {
  transition: all 150ms ease;
}
.button:hover {
  filter: brightness(0.92);
}
.button:active {
  transform: scale(0.98);
}
.button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
.button:disabled {
  opacity: 0.5;
  pointer-events: none;
}
```

## Forms

### Input Field Architecture

```css
.input {
  height: var(--input-height);
  padding: 8px 12px;
  background: var(--color-surface-inset);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-base);
  transition:
    border-color 150ms,
    box-shadow 150ms;
}

.input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px oklch(0.55 0.18 250 / 0.15);
  outline: none;
}

.input-error {
  border-color: var(--color-destructive);
  box-shadow: 0 0 0 3px oklch(0.55 0.22 25 / 0.1);
}
```

### Labels

Always above the field. Font: `--label`. Required indicator: colored dot or asterisk.

```css
.label {
  font: var(--label);
  color: var(--color-text-secondary);
  margin-block-end: var(--space-1);
}
```

### Validation

- Validate inline on blur, not on keypress
- Error messages appear below the field, in `--color-destructive`
- Success state: green border + checkmark icon
- Never remove form data on error
- Group related fields with fieldset/legend

### Multi-Step Forms

- Progress indicator: numbered steps or progress bar
- Each step validated before advancing
- Back button never loses data
- Final step shows summary for review

## Data Tables

### Structure

```css
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  font: var(--label);
  color: var(--color-text-tertiary);
  text-align: start;
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-border-strong);
  white-space: nowrap;
  user-select: none;
}

.table td {
  font: var(--body);
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-border-subtle);
  vertical-align: middle;
}

.table tr:hover td {
  background: var(--color-surface-hover);
}
```

### Features

**Sorting:** Click column header. Arrow icons indicate direction. Active column: bolder text.
**Filtering:** Toolbar above table. Chips for active filters. Clear-all button.
**Pagination:** Below table. Show current range + total. Prefer pagination for >100 rows.
**Row selection:** Checkbox column. Sticky action bar appears on selection.
**Expandable rows:** Chevron + expanded area indented below row.
**Inline editing:** Double-click to edit. Tab to next field. Auto-save on blur.

### Responsive Tables

Under 768px:

- Horizontal scroll with `overflow-x: auto` (preferred for data-dense)
- OR: stacked cards showing key fields only

## Cards

### Metric Card

```css
.metric-card {
  padding: var(--space-4);
  /* label + value + change indicator */
}

.metric-card .label {
  font: var(--label-micro);
  text-transform: uppercase;
}
.metric-card .value {
  font-size: var(--font-size-2xl);
  font-weight: 600;
}
.metric-card .change {
  font-size: var(--font-size-sm);
}
.metric-card .change.positive {
  color: var(--color-success);
}
.metric-card .change.negative {
  color: var(--color-destructive);
}
```

### Feature Card

Title + description + icon. Equal height in grids. Subtle hover lift.

### Settings Card

Section title + description + control (toggle, select). Horizontal layout on desktop.

## Navigation

### Sidebar

```css
.sidebar {
  width: 260px;
  background: var(--color-surface-base);
  border-inline-end: 0.5px solid var(--color-border-default);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-2);
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1.5) var(--space-2);
  border-radius: var(--radius-sm);
  font: var(--body);
  color: var(--color-text-secondary);
  transition:
    background 150ms,
    color 150ms;
}

.sidebar-item:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}

.sidebar-item.active {
  background: var(--color-surface-active);
  color: var(--color-text-primary);
  font-weight: 500;
}
```

### Command Palette (Cmd+K)

- Modal overlay with search input
- Grouped results: actions, pages, recent
- Keyboard navigation: ↑↓ to select, Enter to confirm, Esc to close
- Fuzzy search matching
- Show keyboard shortcuts alongside items

### Tab Systems

```css
.tabs {
  display: flex;
  gap: var(--space-1);
  border-bottom: 1px solid var(--color-border-default);
}

.tab {
  padding: var(--space-2) var(--space-3);
  font: var(--label);
  color: var(--color-text-tertiary);
  border-bottom: 2px solid transparent;
  transition: color 150ms;
}

.tab.active {
  color: var(--color-text-primary);
  border-bottom-color: var(--color-accent);
}
```

## Modals and Dialogs

- Trap focus within modal
- Esc to close
- Click backdrop to close (unless destructive action)
- Maximum width: 480px (small), 640px (medium), 960px (large)
- Sticky header and footer if content scrolls
- Use `<dialog>` element with `showModal()`
- Animate in: scale(0.95) + opacity → scale(1) + opacity

## Toast Notifications

- Fixed position: bottom-right or top-right
- Auto-dismiss: 5 seconds (info), no auto-dismiss (errors)
- Stack from bottom-up, max 3 visible
- Include close button
- Use `role="status"` or `role="alert"` for screen readers

## Empty States

- Centered illustration or icon
- Title explaining what will appear here
- Description with next step
- CTA button for primary action
- Never leave a blank space without explanation

## Loading States

### Skeleton Screens

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface-hover) 25%,
    var(--color-surface-raised) 50%,
    var(--color-surface-hover) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

@keyframes shimmer {
  from {
    background-position: 200% 0;
  }
  to {
    background-position: -200% 0;
  }
}
```

Match skeleton shapes to actual content. Never show a generic spinner for form-like content.

## AI Interface Patterns

### Chat Interface

- User messages right-aligned, assistant left-aligned
- Streaming text: render character-by-character or word-by-word
- Code blocks: syntax highlighting + copy button
- Timestamps subtle, not per-message

### Prompt Input

- Expandable textarea (grows with content)
- Submit button + keyboard shortcut (Cmd+Enter)
- Character/token count indicator
- Attachment support if applicable

### AI Loading

- Typing indicator (animated dots) for short operations < 10s
- Progress bar or step indicator for long operations
- Cancel button for operations > 5s
- Never leave user without feedback
