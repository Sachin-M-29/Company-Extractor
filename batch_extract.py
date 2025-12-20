"""
Batch company extraction to JSON (NDJSON)
- Reads URLs from a CSV/TSV (default expects a column named 'url' or 'website') or a simple text file (one URL per line).
- Scrapes each URL (static by default; optional JS via --js).
- Runs offline LLM via Ollama CLI (CLIExtractor) to produce structured JSON.
- Outputs NDJSON to stdout or a file; optional per-company JSON files.

Usage:
  python batch_extract.py --input companies.csv --output out.ndjson
  python batch_extract.py --input companies.txt --output out.ndjson --per-file out_dir
  python batch_extract.py --input companies.csv --js --model mistral:7b-instruct-q4_0

Notes:
  - This does NOT use the database or UI.
  - Ollama must be installed locally with the chosen model pulled.
"""

import argparse
import csv
import json
import os
import sys
from typing import Iterable, List

from scrapers.scraper import WebScraper, chunk_text
from llm.cli_extractor import CLIExtractor


def read_urls(path: str) -> List[str]:
    urls: List[str] = []
    _, ext = os.path.splitext(path.lower())
    if ext in {".csv", ".tsv"}:
        delim = "\t" if ext == ".tsv" else ","
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delim)
            # Prefer 'url' then 'website', else fall back to first column
            field = None
            for candidate in ("url", "website"):
                if candidate in reader.fieldnames:
                    field = candidate
                    break
            if field is None:
                field = reader.fieldnames[0]
            for row in reader:
                val = (row.get(field) or "").strip()
                if val:
                    urls.append(val)
    else:
        # Plain text, one URL per line
        with open(path, encoding="utf-8") as f:
            for line in f:
                val = line.strip()
                if val:
                    urls.append(val)
    return urls


def scrape_and_extract(url: str, model: str, js: bool, timeout: int) -> dict:
    scraper = WebScraper(timeout=timeout)
    if js:
        import asyncio
        text = asyncio.run(scraper.scrape_js_heavy_page(url))
        if not text:
            text = scraper.scrape_static_html(url)
    else:
        text = scraper.scrape_static_html(url)
    if not text:
        raise RuntimeError(f"Scrape failed: {url}")

    chunks = chunk_text(text, chunk_size=2000, overlap=100)
    content = chunks[0] if chunks else text

    extractor = CLIExtractor(model=model)
    data = extractor.extract_from_text(content, url)
    if not data:
        raise RuntimeError(f"LLM extraction failed: {url}")
    if "website" not in data or not data["website"]:
        data["website"] = url
    return data


def write_ndjson(objs: Iterable[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        for obj in objs:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Batch extract company info to NDJSON using offline LLM")
    parser.add_argument("--input", required=True, help="Input CSV/TSV or txt with URLs")
    parser.add_argument("--output", required=True, help="NDJSON output path")
    parser.add_argument("--model", default="mistral:7b-instruct-q4_0", help="Ollama model")
    parser.add_argument("--js", action="store_true", help="Use Playwright for JS-heavy pages")
    parser.add_argument("--timeout", type=int, default=15, help="Scraping timeout seconds")
    parser.add_argument("--per-file", dest="per_file", help="Optional directory to also write one JSON per URL")

    args = parser.parse_args()

    urls = read_urls(args.input)
    if not urls:
        print("No URLs found in input", file=sys.stderr)
        sys.exit(1)

    if args.per_file:
        os.makedirs(args.per_file, exist_ok=True)

    results = []
    failures = 0
    for url in urls:
        try:
            data = scrape_and_extract(url, model=args.model, js=args.js, timeout=args.timeout)
            results.append(data)
            if args.per_file:
                fname = url.replace("https://", "").replace("http://", "").replace("/", "_") or "company"
                out_path = os.path.join(args.per_file, f"{fname}.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"OK: {url}")
        except Exception as e:
            failures += 1
            print(f"FAIL: {url} -> {e}", file=sys.stderr)

    write_ndjson(results, args.output)
    print(f"\nDone. Saved {len(results)} records to {args.output}. Failures: {failures}")


if __name__ == "__main__":
    main()
