#!/usr/bin/env python3
"""
WCAG and APCA contrast checker for color pairs.
Validates foreground/background combinations against accessibility standards.

Usage:
    python check_contrast.py "#1E293B" "#F8FAFC"
    python check_contrast.py "#1E293B" "#F8FAFC" --level AAA
"""

import sys
import argparse
import json
from math import pow as mpow


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(r, g, b):
    def linearize(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else mpow((c + 0.055) / 1.055, 2.4)

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def wcag_contrast_ratio(fg_hex, bg_hex):
    fg_rgb = hex_to_rgb(fg_hex)
    bg_rgb = hex_to_rgb(bg_hex)

    l1 = relative_luminance(*fg_rgb)
    l2 = relative_luminance(*bg_rgb)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)


def apca_contrast(fg_hex, bg_hex):
    fg_rgb = hex_to_rgb(fg_hex)
    bg_rgb = hex_to_rgb(bg_hex)

    def srgb_to_y(r, g, b):
        def lin(c):
            c = c / 255.0
            return mpow(c, 2.4)
        return 0.2126729 * lin(r) + 0.7151522 * lin(g) + 0.0721750 * lin(b)

    y_text = srgb_to_y(*fg_rgb)
    y_bg = srgb_to_y(*bg_rgb)

    SCALE = 1.14
    OFFSET = 0.027

    if y_bg > y_text:
        sapc = (mpow(y_bg, 0.56) - mpow(y_text, 0.57)) * SCALE
        if sapc < OFFSET:
            return 0.0
        return (sapc - OFFSET) * 100
    else:
        sapc = (mpow(y_bg, 0.65) - mpow(y_text, 0.62)) * SCALE
        if abs(sapc) < OFFSET:
            return 0.0
        return (sapc + OFFSET) * 100


WCAG_THRESHOLDS = {
    "AA": {"normal": 4.5, "large": 3.0},
    "AAA": {"normal": 7.0, "large": 4.5},
}


def check(fg, bg, level="AA"):
    ratio = wcag_contrast_ratio(fg, bg)
    apca = apca_contrast(fg, bg)
    thresholds = WCAG_THRESHOLDS.get(level, WCAG_THRESHOLDS["AA"])

    return {
        "foreground": fg,
        "background": bg,
        "wcag_ratio": round(ratio, 2),
        "apca_score": round(apca, 1),
        "pass_normal": ratio >= thresholds["normal"],
        "pass_large": ratio >= thresholds["large"],
        "level": level,
        "recommendation": _recommend(ratio, apca, level),
    }


def _recommend(ratio, apca, level):
    if ratio >= 7.0:
        return "Excellent contrast — passes AAA for all text sizes"
    if ratio >= 4.5:
        return "Good contrast — passes AA for normal text, AAA for large text"
    if ratio >= 3.0:
        return "Moderate — passes AA for large text only, consider darkening/lightening"
    return "Poor contrast — fails all WCAG levels, must adjust colors"


def format_result(result, fmt="text"):
    if fmt == "json":
        return json.dumps(result, indent=2)

    status_normal = "PASS" if result["pass_normal"] else "FAIL"
    status_large = "PASS" if result["pass_large"] else "FAIL"

    return f"""
╔══════════════════════════════════════════════════════╗
║  CONTRAST CHECK RESULTS                              ║
╠══════════════════════════════════════════════════════╣
║  Foreground:  {result['foreground']:<40}║
║  Background:  {result['background']:<40}║
╠══════════════════════════════════════════════════════╣
║  WCAG Ratio:  {result['wcag_ratio']:<40}║
║  APCA Score:  {result['apca_score']:<40}║
║  Level:       {result['level']:<40}║
╠══════════════════════════════════════════════════════╣
║  Normal Text: {status_normal:<40}║
║  Large Text:  {status_large:<40}║
╠══════════════════════════════════════════════════════╣
║  {result['recommendation']:<52}║
╚══════════════════════════════════════════════════════╝"""


def main():
    parser = argparse.ArgumentParser(description="WCAG/APCA contrast checker")
    parser.add_argument("foreground", help="Foreground color (hex)")
    parser.add_argument("background", help="Background color (hex)")
    parser.add_argument("--level", "-l", choices=["AA", "AAA"], default="AA", help="WCAG level")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text")

    args = parser.parse_args()
    result = check(args.foreground, args.background, args.level)
    print(format_result(result, args.format))


if __name__ == "__main__":
    main()
