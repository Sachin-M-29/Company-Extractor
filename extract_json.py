"""
JSON-only company info extractor
- Scrapes website content (static by default)
- Uses offline LLM via Ollama CLI to extract structured JSON
- Prints JSON to stdout and optionally saves to file

Usage examples:
  python extract_json.py --url https://example.com
  python extract_json.py --url ayadata.ai --output out.json
  python extract_json.py --url https://example.com --model mistral:7b-instruct-q4_0

Requires:
  - Python deps: requests, beautifulsoup4
  - Ollama installed locally with requested model pulled

Note: This script does NOT use the database.
"""

import argparse
import json
import sys
import os

# Ensure local imports work when run directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.scraper import WebScraper, chunk_text
from llm.cli_extractor import CLIExtractor


def extract_company_json(url: str, model: str = "mistral:7b-instruct-q4_0", js: bool = False, timeout: int = 15):
    scraper = WebScraper(timeout=timeout)

    if js:
        import asyncio
        text = asyncio.run(scraper.scrape_js_heavy_page(url))
        if not text:
            # Fallback to static if JS path fails
            text = scraper.scrape_static_html(url)
    else:
        text = scraper.scrape_static_html(url)

    if not text:
        raise RuntimeError(f"Failed to scrape content from {url}")

    chunks = chunk_text(text, chunk_size=2000, overlap=100)
    content = chunks[0] if chunks else text

    extractor = CLIExtractor(model=model)
    data = extractor.extract_from_text(content, url)
    if not data:
        raise RuntimeError("LLM extraction failed")

    # Ensure website field present
    if "website" not in data or data["website"] in (None, ""):
        data["website"] = url

    return data


def main():
    parser = argparse.ArgumentParser(description="Extract company info as JSON using offline LLM")
    parser.add_argument("--url", required=True, help="Company website URL or domain (e.g., https://example.com or example.com)")
    parser.add_argument("--model", default="mistral:7b-instruct-q4_0", help="Ollama model to use (default: mistral:7b-instruct-q4_0)")
    parser.add_argument("--output", help="Optional path to save JSON output")
    parser.add_argument("--js", action="store_true", help="Use Playwright for JS-heavy pages")
    parser.add_argument("--timeout", type=int, default=15, help="Scraping timeout in seconds")

    args = parser.parse_args()

    try:
        result = extract_company_json(args.url, model=args.model, js=args.js, timeout=args.timeout)
        pretty = json.dumps(result, ensure_ascii=False, indent=2)
        print(pretty)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(pretty + "\n")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
