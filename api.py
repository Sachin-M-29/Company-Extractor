"""
Flask API for Company Information Extractor
Bridges Next.js frontend with Python extraction backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper import WebScraper, chunk_text
from utils.resolve import resolve_company_website
from utils.heuristics import extract_all as heuristic_extract
from utils.enrich import enrich_company_details
from llm.hf_extractor import HFExtractor
from database.db import CompanyDatabase

app = Flask(__name__)
CORS(app)

# Database
db = CompanyDatabase()

# Initialize HF Extractor (Mistral 7B)
extractor = HFExtractor(
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    use_gpu=True  # Uses GPU if available
)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Company Extractor API is running'})


@app.route('/api/extract', methods=['POST'])
def extract_single():
    """Extract company information from single URL or company name"""
    try:
        data = request.json
        input_text = data.get('input', '').strip()
        input_type = data.get('input_type', 'url')
        scrape_method = data.get('scrape_method', 'Static HTML Only')
        timeout = int(data.get('timeout', 10))
        enable_enrich = data.get('enable_enrich', False)

        if not input_text:
            return jsonify({'error': 'Input is required'}), 400

        print(f"[API] Extracting: {input_text} (type: {input_type})")

        # Resolve company name to website if needed
        if input_type == 'company':
            print(f"[API] Resolving company name: {input_text}")
            resolved = resolve_company_website(input_text, timeout=timeout)
            if not resolved:
                return jsonify({'error': f"Couldn't find website for '{input_text}'"}), 404
            company_url = resolved
            print(f"[API] Resolved to: {company_url}")
        else:
            company_url = input_text
            if not company_url.lower().startswith(('http://', 'https://')):
                company_url = f'https://{company_url}'

        print(f"[API] Scraping: {company_url}")
        # Scrape website
        scraper = WebScraper(timeout=timeout)
        try:
            if scrape_method == 'Static HTML Only':
                scraped_text = scraper.scrape_static_html(company_url)
            elif scrape_method == 'Auto (Smart)':
                try:
                    scraped_text = scraper.auto_scrape(company_url)
                except Exception as e:
                    print(f"[API] Auto-scrape failed, falling back to static: {e}")
                    scraped_text = scraper.scrape_static_html(company_url)
            else:  # Playwright Only
                try:
                    import asyncio
                    scraped_text = asyncio.run(scraper.scrape_js_heavy_page(company_url))
                except Exception as e:
                    print(f"[API] Playwright failed, falling back to static: {e}")
                    scraped_text = scraper.scrape_static_html(company_url)
        except Exception as e:
            print(f"[API] Scraping error: {e}")
            return jsonify({'error': f'Scraping failed: {str(e)}'}), 500

        if not scraped_text:
            return jsonify({'error': 'Failed to scrape website content'}), 400

        print(f"[API] Scraped {len(scraped_text)} characters, extracting with LLM...")
        # Extract with LLM using global extractor (Mistral 7B via HF)
        chunks = chunk_text(scraped_text, chunk_size=500, overlap=50)
        text_to_extract = chunks[0] if chunks else scraped_text

        extracted_data = extractor.extract_from_text(text_to_extract, company_url)
        if not extracted_data:
            return jsonify({'error': 'LLM extraction failed - is Ollama running?'}), 500

        if not extracted_data.get('website'):
            extracted_data['website'] = company_url

        print(f"[API] Extraction complete, merging heuristics...")
        # Heuristic merge
        try:
            hints = heuristic_extract(company_url, timeout=timeout) or {}
        except Exception as e:
            print(f"[API] Heuristics error: {e}")
            hints = {}

        for k in ['email', 'phone', 'linkedin', 'facebook', 'twitter', 'instagram', 'youtube', 'blog']:
            if not extracted_data.get(k) and hints.get(k):
                extracted_data[k] = hints[k]

        if hints.get('certifications'):
            cur = extracted_data.get('certifications') or []
            if not isinstance(cur, list):
                cur = [cur]
            extracted_data['certifications'] = list(dict.fromkeys([*cur, *hints['certifications']]))

        # Optional enrichment
        if enable_enrich:
            print(f"[API] Enriching details...")
            try:
                enrich = enrich_company_details(company_url, timeout=timeout, fast_mode=True, max_pages=2)
                for k in ['people', 'products', 'services', 'address', 'industry', 'sub_industry', 'sector']:
                    if not extracted_data.get(k) and enrich.get(k):
                        extracted_data[k] = enrich[k]
            except Exception as e:
                print(f"[API] Enrichment error: {e}")

        # Store in database
        try:
            db.insert_company(extracted_data, scrape_url=company_url)
        except Exception as e:
            print(f"[API] Database error: {e}")

        print(f"[API] Success: {extracted_data.get('company_name')}")
        return jsonify(extracted_data)

    except Exception as e:
        print(f"[API] Extract error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'details': str(type(e))}), 500


@app.route('/api/batch-extract', methods=['POST'])
def batch_extract():
    """Extract information from multiple URLs with parallel processing"""
    try:
        data = request.json
        urls = data.get('urls', [])
        scrape_method = data.get('scrape_method', 'Static HTML Only')
        timeout = int(data.get('timeout', 10))
        fast_mode = data.get('fast_mode', True)
        max_workers = int(data.get('max_workers', 3))

        if not urls:
            return jsonify({'error': 'No URLs provided'}), 400

        # Normalize URLs
        normalized_urls = []
        for url in urls:
            url = url.strip()
            if url and not url.lower().startswith(('http://', 'https://')):
                url = f'https://{url}'
            if url:
                normalized_urls.append(url)

        if not normalized_urls:
            return jsonify({'error': 'No valid URLs to process'}), 400

        results = []
        failures = []

        def process_url(url: str):
            """Process single URL"""
            try:
                scraper = WebScraper(timeout=min(timeout, 5) if fast_mode else timeout)
                # Use global extractor (Mistral 7B via HF)

                if scrape_method == 'Static HTML Only':
                    scraped_text = scraper.scrape_static_html(url)
                elif scrape_method == 'Auto (Smart)':
                    try:
                        scraped_text = scraper.auto_scrape(url)
                    except Exception:
                        scraped_text = scraper.scrape_static_html(url)
                else:
                    try:
                        import asyncio
                        scraped_text = asyncio.run(scraper.scrape_js_heavy_page(url))
                    except Exception:
                        scraped_text = scraper.scrape_static_html(url)

                if not scraped_text:
                    raise Exception('Scrape failed')

                chunks = chunk_text(scraped_text, chunk_size=500, overlap=50)
                text_to_extract = chunks[0] if chunks else scraped_text

                extracted_data = extractor.extract_from_text(text_to_extract, url)
                if not extracted_data:
                    raise Exception('LLM extraction failed')

                if not extracted_data.get('website'):
                    extracted_data['website'] = url

                # Heuristic merge
                try:
                    hints = heuristic_extract(url, timeout=min(timeout, 5) if fast_mode else timeout) or {}
                except Exception:
                    hints = {}

                for k in ['email', 'phone', 'linkedin', 'facebook', 'twitter', 'instagram', 'youtube', 'blog']:
                    if not extracted_data.get(k) and hints.get(k):
                        extracted_data[k] = hints[k]

                if hints.get('certifications'):
                    cur = extracted_data.get('certifications') or []
                    if not isinstance(cur, list):
                        cur = [cur]
                    extracted_data['certifications'] = list(dict.fromkeys([*cur, *hints['certifications']]))

                return ('success', extracted_data)
            except Exception as e:
                return ('error', {'url': url, 'error': str(e)})

        # Parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_url, url): url for url in normalized_urls}

            for future in as_completed(futures):
                try:
                    result_type, result_data = future.result()
                    if result_type == 'success':
                        results.append(result_data)
                        # Store in database
                        try:
                            db.insert_company(result_data, scrape_url=result_data.get('website'))
                        except Exception:
                            pass
                    else:
                        failures.append(result_data)
                except Exception as e:
                    failures.append({'url': futures[future], 'error': str(e)})

        return jsonify({
            'results': results,
            'failures': failures,
            'success_count': len(results),
            'failure_count': len(failures),
            'total_count': len(normalized_urls)
        })

    except Exception as e:
        return jsonify({'error': str(e), 'details': str(type(e))}), 500


@app.route('/api/companies', methods=['GET'])
def get_all_companies():
    """Get all extracted companies from database"""
    try:
        limit = int(request.args.get('limit', 500))
        offset = int(request.args.get('offset', 0))

        companies = db.get_all_companies(limit=limit, offset=offset)
        
        # Calculate stats
        total = len(companies)
        avg_confidence = 0
        industries = set()
        
        if companies:
            avg_confidence = sum(c.get('confidence', 0) for c in companies) / len(companies)
            for c in companies:
                if c.get('industry'):
                    industries.add(c.get('industry'))
        
        print(f"[API] Returning {total} companies from database")
        
        return jsonify({
            'companies': companies,
            'stats': {
                'total': total,
                'avg_confidence': round(avg_confidence, 2),
                'industries_found': len(industries)
            }
        })
    except Exception as e:
        print(f"[API] Error fetching companies: {e}")
        return jsonify({'error': str(e), 'companies': []}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
