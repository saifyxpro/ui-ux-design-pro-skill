#!/usr/bin/env python3
"""
Modular type scale calculator.
Generates typographic scales using musical ratios.

Usage:
    python generate_typography.py --base 16 --ratio 1.25 --steps 8
    python generate_typography.py --scale golden
"""

import argparse
import json

NAMED_RATIOS = {
    "minor-second": 1.067,
    "major-second": 1.125,
    "minor-third": 1.2,
    "major-third": 1.25,
    "perfect-fourth": 1.333,
    "augmented-fourth": 1.414,
    "perfect-fifth": 1.5,
    "golden": 1.618,
}

STEP_NAMES = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl"]


def generate_scale(base_px=16, ratio=1.25, steps=8):
    scale = []
    for i in range(-2, steps - 2):
        size_px = base_px * (ratio ** i)
        name = STEP_NAMES[i + 2] if i + 2 < len(STEP_NAMES) else f"step-{i + 2}"
        lh = max(1.1, 1.5 - (i * 0.05)) if i >= 0 else 1.6
        scale.append({
            "name": name,
            "px": round(size_px, 2),
            "rem": round(size_px / 16, 4),
            "line_height": round(lh, 2),
            "ratio_step": i,
        })
    return scale


def format_scale(scale, ratio_name, fmt="css"):
    if fmt == "json":
        return json.dumps({"ratio": ratio_name, "scale": scale}, indent=2)

    if fmt == "css":
        lines = [f"/* Type Scale: {ratio_name} */", ":root {"]
        for s in scale:
            lines.append(f"  --text-{s['name']}: {s['rem']}rem; /* {s['px']}px */")
        lines.append("")
        for s in scale:
            lines.append(f"  --leading-{s['name']}: {s['line_height']};")
        lines.append("}")
        return "\n".join(lines)

    lines = [f"\n  Scale: {ratio_name}", ""]
    lines.append(f"  {'Name':<8} {'px':<10} {'rem':<10} {'Line Height':<12}")
    lines.append(f"  {'─'*8} {'─'*10} {'─'*10} {'─'*12}")
    for s in scale:
        lines.append(f"  {s['name']:<8} {s['px']:<10} {s['rem']:<10} {s['line_height']:<12}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Modular type scale calculator")
    parser.add_argument("--base", "-b", type=float, default=16, help="Base font size in px")
    parser.add_argument("--ratio", "-r", type=float, default=1.25, help="Scale ratio")
    parser.add_argument("--scale", "-s", choices=list(NAMED_RATIOS.keys()), help="Named scale")
    parser.add_argument("--steps", "-n", type=int, default=8, help="Number of steps")
    parser.add_argument("--format", "-f", choices=["text", "json", "css"], default="css")

    args = parser.parse_args()
    ratio = NAMED_RATIOS[args.scale] if args.scale else args.ratio
    ratio_name = args.scale or f"custom ({ratio})"

    scale = generate_scale(args.base, ratio, args.steps)
    print(format_scale(scale, ratio_name, args.format))


if __name__ == "__main__":
    main()
