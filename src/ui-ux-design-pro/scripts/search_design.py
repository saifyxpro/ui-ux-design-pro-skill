#!/usr/bin/env python3
"""
BM25 search engine for UI/UX design databases.
Searches across styles, typography, charts, colors, reasoning, UX guidelines, and tech stacks.

Usage:
    python search_design.py "SaaS dashboard" --domain style --max-results 5
    python search_design.py "dark mode fintech" --stack nextjs
"""

import csv
import re
import sys
import io
import json
import argparse
from pathlib import Path
from math import log
from collections import defaultdict

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = Path(__file__).parent.parent / "data"
DEFAULT_MAX_RESULTS = 3

BM25_K1 = 1.5
BM25_B = 0.75

DOMAIN_FILES = {
    "style": "styles.csv",
    "color": "colors.csv",
    "chart": "charts.csv",
    "typography": "typography.csv",
    "reasoning": "ui-reasoning.csv",
    "ux": "ux-guidelines.csv",
    "product": "products.csv",
    "icon": "icons.csv",
    "landing": "landing.csv",
    "performance": "react-performance.csv",
    "web": "web-interface.csv",
}

_cache = {}


def tokenize(text):
    return re.findall(r'\w+', text.lower())


def load_csv(filepath):
    if str(filepath) in _cache:
        return _cache[str(filepath)]

    rows = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                combined = " ".join(str(v) for v in row.values())
                rows.append({"data": dict(row), "tokens": tokenize(combined), "text": combined})
    except FileNotFoundError:
        pass

    _cache[str(filepath)] = rows
    return rows


def bm25_score(query_tokens, documents):
    doc_count = len(documents)
    if doc_count == 0:
        return []

    avg_dl = sum(len(d["tokens"]) for d in documents) / doc_count

    df = defaultdict(int)
    for doc in documents:
        seen = set(doc["tokens"])
        for term in seen:
            df[term] += 1

    scores = []
    for doc in documents:
        score = 0.0
        dl = len(doc["tokens"])
        tf_map = defaultdict(int)
        for t in doc["tokens"]:
            tf_map[t] += 1

        for qt in query_tokens:
            if df[qt] == 0:
                continue
            idf = log((doc_count - df[qt] + 0.5) / (df[qt] + 0.5) + 1.0)
            tf = tf_map[qt]
            numerator = tf * (BM25_K1 + 1)
            denominator = tf + BM25_K1 * (1 - BM25_B + BM25_B * (dl / avg_dl))
            score += idf * (numerator / denominator)

        scores.append((score, doc))

    scores.sort(key=lambda x: x[0], reverse=True)
    return scores


def search(query, domain=None, stack=None, max_results=DEFAULT_MAX_RESULTS):
    query_tokens = tokenize(query)
    results = {}

    if stack:
        stack_file = DATA_DIR / "stacks" / f"{stack.lower()}.csv"
        docs = load_csv(stack_file)
        if docs:
            scored = bm25_score(query_tokens, docs)
            results["stack"] = [(s, d["data"]) for s, d in scored[:max_results] if s > 0]

    if domain:
        domains = [domain] if domain in DOMAIN_FILES else list(DOMAIN_FILES.keys())
    else:
        domains = list(DOMAIN_FILES.keys())

    for dom in domains:
        filepath = DATA_DIR / DOMAIN_FILES[dom]
        docs = load_csv(filepath)
        if not docs:
            continue
        scored = bm25_score(query_tokens, docs)
        top = [(s, d["data"]) for s, d in scored[:max_results] if s > 0]
        if top:
            results[dom] = top

    return results


def format_results(results, output_format="text"):
    if output_format == "json":
        out = {}
        for domain, items in results.items():
            out[domain] = [{"score": round(s, 3), **data} for s, data in items]
        return json.dumps(out, indent=2, ensure_ascii=False)

    lines = []
    for domain, items in results.items():
        lines.append(f"\n{'='*60}")
        lines.append(f"  {domain.upper()} RESULTS")
        lines.append(f"{'='*60}")
        for i, (score, data) in enumerate(items, 1):
            lines.append(f"\n  #{i} (score: {score:.3f})")
            for key, val in data.items():
                if val and str(val).strip():
                    lines.append(f"    {key}: {val}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="BM25 search engine for UI/UX design databases")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--domain", "-d", choices=list(DOMAIN_FILES.keys()), help="Restrict to domain")
    parser.add_argument("--stack", "-s", help="Tech stack name (e.g. nextjs, react, angular)")
    parser.add_argument("--max-results", "-n", type=int, default=DEFAULT_MAX_RESULTS, help="Max results per domain")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()
    results = search(args.query, domain=args.domain, stack=args.stack, max_results=args.max_results)

    if not results:
        print(f"No results found for: {args.query}")
        sys.exit(1)

    print(format_results(results, args.format))


if __name__ == "__main__":
    main()
