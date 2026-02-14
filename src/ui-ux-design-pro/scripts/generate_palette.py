#!/usr/bin/env python3
"""
Color harmony and palette generator.
Generates harmonious color palettes from a base color using color theory.

Usage:
    python generate_palette.py "#2563EB" --harmony triadic --count 5
    python generate_palette.py "#2563EB" --harmony complementary
"""

import argparse
import json
import sys
from math import fmod


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

    return h * 360, s * 100, l * 100


def hsl_to_hex(h, s, l):
    h, s, l = h / 360.0, s / 100.0, l / 100.0

    if s == 0:
        r = g = b = l
    else:
        def hue_to_rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255)).upper()


HARMONY_OFFSETS = {
    "complementary": [180],
    "analogous": [-30, 30],
    "triadic": [120, 240],
    "tetradic": [90, 180, 270],
    "split-complementary": [150, 210],
    "monochromatic": [],
}


def generate_palette(base_hex, harmony="triadic", count=5):
    h, s, l = hex_to_hsl(base_hex)
    colors = [{"hex": base_hex.upper(), "role": "base", "hsl": f"hsl({h:.0f}, {s:.0f}%, {l:.0f}%)"}]

    offsets = HARMONY_OFFSETS.get(harmony, [])

    for offset in offsets:
        new_h = fmod(h + offset, 360)
        hex_val = hsl_to_hex(new_h, s, l)
        colors.append({
            "hex": hex_val,
            "role": f"+{offset}°",
            "hsl": f"hsl({new_h:.0f}, {s:.0f}%, {l:.0f}%)",
        })

    if harmony == "monochromatic":
        for i in range(1, count):
            new_l = max(10, min(95, l + (i - count // 2) * 12))
            hex_val = hsl_to_hex(h, s, new_l)
            colors.append({
                "hex": hex_val,
                "role": f"L{new_l:.0f}",
                "hsl": f"hsl({h:.0f}, {s:.0f}%, {new_l:.0f}%)",
            })

    while len(colors) < count:
        idx = len(colors) - 1
        existing_h = hex_to_hsl(colors[idx]["hex"])[0]
        lighter_l = min(95, l + 20)
        colors.append({
            "hex": hsl_to_hex(existing_h, s, lighter_l),
            "role": "light variant",
            "hsl": f"hsl({existing_h:.0f}, {s:.0f}%, {lighter_l:.0f}%)",
        })

    return colors[:count]


def format_palette(colors, harmony, fmt="text"):
    if fmt == "json":
        return json.dumps({"harmony": harmony, "palette": colors}, indent=2)

    if fmt == "css":
        lines = [":root {"]
        for i, c in enumerate(colors):
            lines.append(f"  --palette-{i}: {c['hex']};")
        lines.append("}")
        return "\n".join(lines)

    lines = [f"\n  Harmony: {harmony}", f"  Colors: {len(colors)}", ""]
    for i, c in enumerate(colors):
        block = "██████"
        lines.append(f"  {block}  {c['hex']}  ({c['role']})  {c['hsl']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Color harmony palette generator")
    parser.add_argument("color", help="Base color (hex)")
    parser.add_argument("--harmony", "-H", choices=list(HARMONY_OFFSETS.keys()),
                        default="triadic", help="Harmony type")
    parser.add_argument("--count", "-c", type=int, default=5, help="Number of colors")
    parser.add_argument("--format", "-f", choices=["text", "json", "css"], default="text")

    args = parser.parse_args()
    palette = generate_palette(args.color, args.harmony, args.count)
    print(format_palette(palette, args.harmony, args.format))


if __name__ == "__main__":
    main()
