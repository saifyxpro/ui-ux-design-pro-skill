#!/usr/bin/env python3
"""
UI/UX Design Pro — Main CLI Entry Point.
Routes subcommands to individual scripts.

Usage:
    python design_cli.py search "SaaS dashboard" --domain style
    python design_cli.py contrast "#1E293B" "#F8FAFC"
    python design_cli.py palette "#2563EB" --harmony triadic
    python design_cli.py tokens --preset fintech
    python design_cli.py typography --scale golden
    python design_cli.py system "fintech dashboard" --stack nextjs
    python design_cli.py audit /path/to/file.tsx
"""

import sys
import os
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

COMMANDS = {
    "search": {
        "script": "search_design.py",
        "help": "BM25 search across all design databases",
        "example": 'search "dark mode SaaS" --domain style',
    },
    "contrast": {
        "script": "check_contrast.py",
        "help": "WCAG/APCA contrast checker for color pairs",
        "example": 'contrast "#1E293B" "#F8FAFC" --level AAA',
    },
    "palette": {
        "script": "generate_palette.py",
        "help": "Color harmony palette generator",
        "example": 'palette "#2563EB" --harmony triadic --count 5',
    },
    "tokens": {
        "script": "generate_tokens.py",
        "help": "CSS custom property / design token generator",
        "example": "tokens --preset fintech --format css",
    },
    "typography": {
        "script": "generate_typography.py",
        "help": "Modular type scale calculator",
        "example": "typography --scale golden --format css",
    },
    "system": {
        "script": "generate_system.py",
        "help": "Full design system generator with BM25 search",
        "example": 'system "healthcare portal" --stack nextjs',
    },
    "audit": {
        "script": "audit_ui.py",
        "help": "UI code quality and accessibility auditor",
        "example": "audit ./src/App.tsx",
    },
}

BANNER = """
╔══════════════════════════════════════════════════════╗
║  UI/UX Design Pro — Design Intelligence CLI          ║
║  v2.0.0 | 1,875 data rows | 27 CSV databases        ║
╚══════════════════════════════════════════════════════╝
"""


def print_help():
    print(BANNER)
    print("  Commands:\n")
    for name, info in COMMANDS.items():
        print(f"    {name:<12} {info['help']}")
    print("\n  Examples:\n")
    for name, info in COMMANDS.items():
        print(f"    python design_cli.py {info['example']}")
    print()


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    command = sys.argv[1]

    if command not in COMMANDS:
        print(f"  Unknown command: {command}")
        print(f"  Available: {', '.join(COMMANDS.keys())}")
        sys.exit(1)

    script_path = SCRIPTS_DIR / COMMANDS[command]["script"]
    if not script_path.exists():
        print(f"  Script not found: {script_path}")
        sys.exit(1)

    args = [sys.executable, str(script_path)] + sys.argv[2:]

    try:
        result = subprocess.run(args, check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
