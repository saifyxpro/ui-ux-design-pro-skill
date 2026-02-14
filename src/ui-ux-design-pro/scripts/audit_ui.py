#!/usr/bin/env python3
"""
UI code quality auditor.
Scans HTML/CSS/JSX files for common UI anti-patterns and accessibility issues.

Usage:
    python audit_ui.py /path/to/component.tsx
    python audit_ui.py /path/to/styles.css --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path

SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_WARNING = "WARNING"
SEVERITY_INFO = "INFO"

RULES = [
    {
        "id": "A001",
        "name": "missing-alt-text",
        "pattern": r'<img(?![^>]*alt=)[^>]*>',
        "severity": SEVERITY_CRITICAL,
        "message": "Image missing alt attribute — WCAG 1.1.1 violation",
        "fix": 'Add alt="" for decorative images or descriptive alt text for informational images',
    },
    {
        "id": "A002",
        "name": "missing-aria-label",
        "pattern": r'<button(?![^>]*(?:aria-label|aria-labelledby))[^>]*>\s*<(?:svg|img|i|span)',
        "severity": SEVERITY_WARNING,
        "message": "Icon-only button without aria-label",
        "fix": "Add aria-label describing the button action",
    },
    {
        "id": "A003",
        "name": "hardcoded-color",
        "pattern": r'(?:color|background|border):\s*#[0-9a-fA-F]{3,8}',
        "severity": SEVERITY_INFO,
        "message": "Hardcoded color value — use design tokens instead",
        "fix": "Replace with CSS custom property: var(--color-primary-500)",
    },
    {
        "id": "A004",
        "name": "px-font-size",
        "pattern": r'font-size:\s*\d+px',
        "severity": SEVERITY_WARNING,
        "message": "Font size in px — use rem for accessibility",
        "fix": "Convert to rem: 16px = 1rem",
    },
    {
        "id": "A005",
        "name": "magic-z-index",
        "pattern": r'z-index:\s*(?:999|9999|99999)',
        "severity": SEVERITY_WARNING,
        "message": "Magic z-index value — use token scale",
        "fix": "Define z-index tokens: --z-dropdown: 100, --z-modal: 200, --z-toast: 300",
    },
    {
        "id": "A006",
        "name": "important-override",
        "pattern": r'!important',
        "severity": SEVERITY_WARNING,
        "message": "!important override detected — indicates specificity issues",
        "fix": "Refactor CSS specificity instead of using !important",
    },
    {
        "id": "A007",
        "name": "inline-style",
        "pattern": r'style=\{?\{[^}]+\}\}?|style="[^"]*"',
        "severity": SEVERITY_INFO,
        "message": "Inline style detected — extract to CSS module or styled-component",
        "fix": "Move styles to external stylesheet or CSS-in-JS",
    },
    {
        "id": "A008",
        "name": "missing-focus-visible",
        "pattern": r':focus\s*\{[^}]*outline:\s*(?:none|0)',
        "severity": SEVERITY_CRITICAL,
        "message": "Focus outline removed — WCAG 2.4.7 violation",
        "fix": "Use :focus-visible instead and provide visible focus indicator",
    },
    {
        "id": "A009",
        "name": "low-tap-target",
        "pattern": r'(?:width|height|min-width|min-height):\s*(?:[1-3][0-9]|[0-9])px',
        "severity": SEVERITY_WARNING,
        "message": "Potential low tap target — minimum 44px recommended",
        "fix": "Ensure interactive elements are at least 44x44px",
    },
    {
        "id": "A010",
        "name": "missing-lang",
        "pattern": r'<html(?![^>]*lang=)',
        "severity": SEVERITY_CRITICAL,
        "message": "HTML element missing lang attribute",
        "fix": 'Add lang="en" (or appropriate language) to <html>',
    },
    {
        "id": "A011",
        "name": "autoplaying-media",
        "pattern": r'<(?:video|audio)(?=[^>]*autoplay)',
        "severity": SEVERITY_WARNING,
        "message": "Autoplaying media — may cause accessibility issues",
        "fix": "Add muted attribute or provide pause controls",
    },
    {
        "id": "A012",
        "name": "color-only-indicator",
        "pattern": r'(?:color|background-color):\s*(?:red|green|#(?:f00|0f0|ff0000|00ff00))',
        "severity": SEVERITY_WARNING,
        "message": "Color-only status indicator — add icon or text for colorblind users",
        "fix": "Add supporting icon, text, or pattern to convey meaning",
    },
]


def audit_file(filepath):
    content = Path(filepath).read_text(encoding="utf-8")
    lines = content.split("\n")
    findings = []

    for rule in RULES:
        pattern = re.compile(rule["pattern"], re.IGNORECASE)
        for line_num, line in enumerate(lines, 1):
            if pattern.search(line):
                findings.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "line": line_num,
                    "code": line.strip()[:80],
                    "message": rule["message"],
                    "fix": rule["fix"],
                })

    return findings


def format_findings(findings, filepath, fmt="text"):
    if fmt == "json":
        return json.dumps({"file": str(filepath), "findings": findings, "count": len(findings)}, indent=2)

    critical = sum(1 for f in findings if f["severity"] == SEVERITY_CRITICAL)
    warnings = sum(1 for f in findings if f["severity"] == SEVERITY_WARNING)
    info = sum(1 for f in findings if f["severity"] == SEVERITY_INFO)

    lines = [
        f"\n  UI AUDIT: {filepath}",
        f"  {critical} critical | {warnings} warnings | {info} info",
        "",
    ]

    for f in sorted(findings, key=lambda x: (x["severity"] != SEVERITY_CRITICAL, x["line"])):
        icon = "🔴" if f["severity"] == SEVERITY_CRITICAL else "🟡" if f["severity"] == SEVERITY_WARNING else "🔵"
        lines.append(f"  {icon} L{f['line']} [{f['rule_id']}] {f['message']}")
        lines.append(f"     Code: {f['code']}")
        lines.append(f"     Fix:  {f['fix']}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="UI code quality auditor")
    parser.add_argument("files", nargs="+", help="Files to audit")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text")

    args = parser.parse_args()

    total_findings = 0
    for filepath in args.files:
        p = Path(filepath)
        if not p.exists():
            print(f"  File not found: {filepath}")
            continue
        findings = audit_file(filepath)
        total_findings += len(findings)
        print(format_findings(findings, filepath, args.format))

    if total_findings == 0:
        print("\n  No issues found!")


if __name__ == "__main__":
    main()
