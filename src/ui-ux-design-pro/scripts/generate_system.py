#!/usr/bin/env python3
"""
Design System Generator.
Aggregates BM25 search results with industry reasoning to produce
a comprehensive design system recommendation with persistence.

Usage:
    python generate_system.py "fintech dashboard" --stack nextjs --output design-system.json
    python generate_system.py "healthcare portal" --format css
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from search_design import search, tokenize, load_csv, bm25_score, DATA_DIR
from generate_tokens import generate_all, format_css, hex_to_hsl
from generate_palette import generate_palette
from generate_typography import generate_scale, NAMED_RATIOS, format_scale

SEARCH_CONFIG = {
    "product": {"max_results": 1},
    "style": {"max_results": 3},
    "color": {"max_results": 2},
    "landing": {"max_results": 2},
    "typography": {"max_results": 2},
    "reasoning": {"max_results": 2},
    "ux": {"max_results": 3},
    "chart": {"max_results": 2},
}


def extract_primary_color(search_results):
    for domain in ["color", "style", "product"]:
        if domain in search_results:
            for score, data in search_results[domain]:
                for key in ["Primary", "Primary (Hex)", "Primary Colors", "primary"]:
                    if key in data and data[key]:
                        val = str(data[key]).strip().strip('"')
                        if val.startswith("#"):
                            return val
    return "#2563EB"


def extract_font(search_results):
    if "typography" in search_results:
        for score, data in search_results["typography"]:
            for key in ["Heading Font", "heading", "Font Pairing Name"]:
                if key in data and data[key]:
                    return str(data[key]).strip().strip('"')
    return "Inter"


def extract_style(search_results):
    if "style" in search_results:
        for score, data in search_results["style"]:
            for key in ["Style Category", "style_category", "name"]:
                if key in data and data[key]:
                    return str(data[key]).strip().strip('"')
    return "Modern Minimal"


def extract_reasoning(search_results):
    rules = []
    if "reasoning" in search_results:
        for score, data in search_results["reasoning"]:
            rules.append({
                "category": data.get("UI_Category", "General"),
                "pattern": data.get("Recommended_Pattern", ""),
                "anti_patterns": data.get("Anti_Patterns", ""),
            })
    return rules


def extract_ux_guidelines(search_results):
    guidelines = []
    if "ux" in search_results:
        for score, data in search_results["ux"]:
            guidelines.append({
                "category": data.get("Category", ""),
                "issue": data.get("Issue", ""),
                "do": data.get("Do", ""),
                "dont": data.get("Don't", data.get("Dont", "")),
            })
    return guidelines


def generate_system(query, stack=None):
    all_results = {}
    for domain, config in SEARCH_CONFIG.items():
        results = search(query, domain=domain, max_results=config["max_results"])
        if domain in results:
            all_results[domain] = results[domain]

    if stack:
        stack_results = search(query, stack=stack, max_results=3)
        if "stack" in stack_results:
            all_results["stack"] = stack_results["stack"]

    primary_color = extract_primary_color(all_results)
    font_family = extract_font(all_results)
    style_name = extract_style(all_results)
    reasoning = extract_reasoning(all_results)
    ux_guidelines = extract_ux_guidelines(all_results)

    tokens = generate_all(primary=primary_color, font=font_family)
    palette = generate_palette(primary_color, harmony="triadic", count=5)
    type_scale = generate_scale(base_px=16, ratio=1.25)

    system = {
        "meta": {
            "query": query,
            "stack": stack,
            "generated_at": datetime.now().isoformat(),
            "version": "2.0.0",
        },
        "style": {
            "name": style_name,
            "primary_color": primary_color,
            "font_family": font_family,
        },
        "tokens": tokens,
        "palette": [c for c in palette],
        "type_scale": type_scale,
        "reasoning": reasoning,
        "ux_guidelines": ux_guidelines,
        "search_sources": {
            domain: [{"score": round(s, 3)} for s, _ in items]
            for domain, items in all_results.items()
        },
    }

    return system


def format_system(system, fmt="json"):
    if fmt == "json":
        return json.dumps(system, indent=2, ensure_ascii=False, default=str)

    if fmt == "css":
        return format_css(system["tokens"])

    lines = [
        f"  Design System: {system['style']['name']}",
        f"  Query: {system['meta']['query']}",
        f"  Stack: {system['meta']['stack'] or 'any'}",
        f"  Primary: {system['style']['primary_color']}",
        f"  Font: {system['style']['font_family']}",
        "",
        f"  Tokens: {len(system['tokens'])} custom properties",
        f"  Palette: {len(system['palette'])} colors",
        f"  Type Scale: {len(system['type_scale'])} steps",
        f"  Reasoning Rules: {len(system['reasoning'])}",
        f"  UX Guidelines: {len(system['ux_guidelines'])}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Design system generator with BM25 search")
    parser.add_argument("query", help="Design context query")
    parser.add_argument("--stack", "-s", help="Tech stack (e.g. nextjs, react)")
    parser.add_argument("--format", "-f", choices=["json", "css", "text"], default="json")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()
    system = generate_system(args.query, args.stack)
    output = format_system(system, args.format)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"  Design system saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
