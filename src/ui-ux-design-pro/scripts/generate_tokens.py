#!/usr/bin/env python3
"""
CSS Custom Property (design token) generator.
Generates a complete token system from search results or manual input.

Usage:
    python generate_tokens.py --primary "#2563EB" --neutral "#64748B" --radius 12
    python generate_tokens.py --preset fintech
"""

import argparse
import json
import sys
from math import pow as mpow


PRESETS = {
    "fintech": {"primary": "#2563EB", "neutral": "#64748B", "radius": 8, "font": "Inter"},
    "healthcare": {"primary": "#059669", "neutral": "#6B7280", "radius": 12, "font": "Source Sans Pro"},
    "ecommerce": {"primary": "#DC2626", "neutral": "#78716C", "radius": 8, "font": "Poppins"},
    "saas": {"primary": "#7C3AED", "neutral": "#6B7280", "radius": 12, "font": "Inter"},
    "education": {"primary": "#2563EB", "neutral": "#9CA3AF", "radius": 16, "font": "Nunito"},
    "gaming": {"primary": "#EF4444", "neutral": "#374151", "radius": 4, "font": "Orbitron"},
    "luxury": {"primary": "#1E293B", "neutral": "#94A3B8", "radius": 0, "font": "Playfair Display"},
    "startup": {"primary": "#8B5CF6", "neutral": "#6B7280", "radius": 12, "font": "DM Sans"},
}


def hex_to_hsl(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2.0

    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6.0

    return round(h * 360), round(s * 100), round(l * 100)


def generate_scale(hex_color, name="primary"):
    h, s, _ = hex_to_hsl(hex_color)
    lightness_steps = {
        50: 97, 100: 94, 200: 86, 300: 77, 400: 66,
        500: 50, 600: 41, 700: 35, 800: 27, 900: 20, 950: 12,
    }
    tokens = {}
    for step, l in lightness_steps.items():
        tokens[f"--color-{name}-{step}"] = f"hsl({h}, {s}%, {l}%)"
    return tokens


def generate_spacing():
    base = 4
    steps = {
        "0": "0px", "px": "1px", "0.5": f"{base * 0.5}px", "1": f"{base}px",
        "1.5": f"{base * 1.5}px", "2": f"{base * 2}px", "2.5": f"{base * 2.5}px",
        "3": f"{base * 3}px", "4": f"{base * 4}px", "5": f"{base * 5}px",
        "6": f"{base * 6}px", "8": f"{base * 8}px", "10": f"{base * 10}px",
        "12": f"{base * 12}px", "16": f"{base * 16}px", "20": f"{base * 20}px",
        "24": f"{base * 24}px", "32": f"{base * 32}px", "40": f"{base * 40}px",
        "48": f"{base * 48}px", "64": f"{base * 64}px",
    }
    return {f"--spacing-{k}": v for k, v in steps.items()}


def generate_typography_tokens(font_family="Inter"):
    return {
        "--font-family-heading": f"'{font_family}', system-ui, sans-serif",
        "--font-family-body": f"'{font_family}', system-ui, sans-serif",
        "--font-family-mono": "'JetBrains Mono', 'Fira Code', monospace",
        "--font-size-xs": "0.75rem",
        "--font-size-sm": "0.875rem",
        "--font-size-base": "1rem",
        "--font-size-lg": "1.125rem",
        "--font-size-xl": "1.25rem",
        "--font-size-2xl": "1.5rem",
        "--font-size-3xl": "1.875rem",
        "--font-size-4xl": "2.25rem",
        "--font-size-5xl": "3rem",
        "--font-size-6xl": "3.75rem",
        "--line-height-tight": "1.25",
        "--line-height-normal": "1.5",
        "--line-height-relaxed": "1.75",
        "--font-weight-normal": "400",
        "--font-weight-medium": "500",
        "--font-weight-semibold": "600",
        "--font-weight-bold": "700",
    }


def generate_radius_tokens(base_radius=12):
    return {
        "--radius-none": "0px",
        "--radius-sm": f"{max(base_radius - 4, 2)}px",
        "--radius-md": f"{base_radius}px",
        "--radius-lg": f"{base_radius + 4}px",
        "--radius-xl": f"{base_radius + 8}px",
        "--radius-2xl": f"{base_radius + 16}px",
        "--radius-full": "9999px",
    }


def generate_shadow_tokens():
    return {
        "--shadow-xs": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        "--shadow-sm": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        "--shadow-md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        "--shadow-lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
        "--shadow-xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
        "--shadow-2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)",
    }


def generate_animation_tokens():
    return {
        "--duration-fast": "150ms",
        "--duration-normal": "300ms",
        "--duration-slow": "500ms",
        "--easing-default": "cubic-bezier(0.4, 0, 0.2, 1)",
        "--easing-in": "cubic-bezier(0.4, 0, 1, 1)",
        "--easing-out": "cubic-bezier(0, 0, 0.2, 1)",
        "--easing-bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
    }


def generate_all(primary="#2563EB", neutral="#64748B", radius=12, font="Inter"):
    tokens = {}
    tokens.update(generate_scale(primary, "primary"))
    tokens.update(generate_scale(neutral, "neutral"))
    tokens.update(generate_spacing())
    tokens.update(generate_typography_tokens(font))
    tokens.update(generate_radius_tokens(radius))
    tokens.update(generate_shadow_tokens())
    tokens.update(generate_animation_tokens())
    return tokens


def format_css(tokens):
    lines = [":root {"]
    current_group = ""
    for key, val in tokens.items():
        group = key.split("-")[1] if "-" in key else ""
        if group != current_group:
            if current_group:
                lines.append("")
            current_group = group
        lines.append(f"  {key}: {val};")
    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CSS design token generator")
    parser.add_argument("--primary", "-p", default="#2563EB", help="Primary color hex")
    parser.add_argument("--neutral", "-n", default="#64748B", help="Neutral color hex")
    parser.add_argument("--radius", "-r", type=int, default=12, help="Base border radius")
    parser.add_argument("--font", "-t", default="Inter", help="Base font family")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="Use a preset")
    parser.add_argument("--format", "-f", choices=["css", "json"], default="css")

    args = parser.parse_args()

    if args.preset:
        p = PRESETS[args.preset]
        tokens = generate_all(p["primary"], p["neutral"], p["radius"], p["font"])
    else:
        tokens = generate_all(args.primary, args.neutral, args.radius, args.font)

    if args.format == "json":
        print(json.dumps(tokens, indent=2))
    else:
        print(format_css(tokens))


if __name__ == "__main__":
    main()
