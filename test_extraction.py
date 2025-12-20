#!/usr/bin/env python3
"""
Test extraction directly
"""
import sys
sys.path.insert(0, '/c/projects/data/web-scraper-llm')

from scrapers.scraper import WebScraper, chunk_text
from llm.cli_extractor import CLIExtractor

# Test scraping
print("[TEST] Starting extraction test...")
print("[TEST] Step 1: Scraping Google.com...")

scraper = WebScraper(timeout=5)
try:
    content = scraper.scrape_static_html('https://google.com')
    print(f"[TEST] Scraped {len(content)} characters")
except Exception as e:
    print(f"[TEST] Scraping failed: {e}")
    sys.exit(1)

# Test LLM
print("[TEST] Step 2: Testing LLM extraction...")
extractor = CLIExtractor()
chunks = chunk_text(content, chunk_size=500, overlap=50)
text_to_extract = chunks[0] if chunks else content

try:
    result = extractor.extract_from_text(text_to_extract[:2000], 'https://google.com')
    if result:
        print(f"[TEST] LLM Success! Company: {result.get('company_name')}")
    else:
        print("[TEST] LLM returned None")
except Exception as e:
    print(f"[TEST] LLM extraction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("[TEST] All tests passed!")
