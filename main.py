"""
Main entry point for Web Scraper + LLM Information Extraction System
Supports CLI and programmatic usage
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, List

from scrapers.scraper import WebScraper, chunk_text
from llm.extractor import LLMExtractor
from database.db import CompanyDatabase
import config


def scrape_and_extract(url: str, scrape_method: str = "auto", 
                      save_to_db: bool = True) -> Optional[dict]:
    """
    Complete pipeline: scrape → extract → save
    
    Args:
        url: Website URL to process
        scrape_method: "auto", "static", or "playwright"
        save_to_db: Save results to database
        
    Returns:
        Extracted data dict or None
    """
    print(f"\n{'='*60}")
    print(f"Processing: {url}")
    print(f"{'='*60}")
    
    # Initialize components
    scraper = WebScraper(timeout=config.SCRAPE_TIMEOUT)
    extractor = LLMExtractor(
        model=config.OLLAMA_MODEL,
        ollama_host=config.OLLAMA_HOST
    )
    
    # Step 1: Scrape
    print(f"\n[1/3] Scraping website...")
    if scrape_method == "auto":
        text = scraper.auto_scrape(url)
    elif scrape_method == "static":
        text = scraper.scrape_static_html(url)
    else:  # playwright
        text = asyncio.run(scraper.scrape_js_heavy_page(url))
    
    if not text:
        print("❌ Scraping failed!")
        return None
    
    print(f"✓ Scraped {len(text):,} characters")
    
    # Step 2: Chunk
    print(f"\n[2/3] Chunking text...")
    chunks = chunk_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Step 3: Extract
    print(f"\n[3/3] Extracting information with LLM...")
    data = extractor.extract_from_text(chunks[0], url)
    
    if not data:
        print("❌ Extraction failed!")
        return None
    
    print(f"✓ Extraction successful")
    
    # Display results
    print(f"\n{'─'*60}")
    print(f"Company: {data.get('company_name', 'N/A')}")
    print(f"Industry: {data.get('industry', 'N/A')}")
    print(f"Confidence: {data.get('confidence', 0):.0%}")
    print(f"Email: {data.get('email', 'N/A')}")
    print(f"Phone: {data.get('phone', 'N/A')}")
    print(f"Address: {data.get('address', 'N/A')}")
    if data.get('products'):
        print(f"Products: {', '.join(data['products'])}")
    print(f"{'─'*60}")
    
    # Save to database
    if save_to_db:
        db = CompanyDatabase()
        company_id = db.insert_company(
            data,
            scrape_url=url,
            scrape_method=scrape_method,
            content_length=len(text),
            processing_time=0,
            raw_content=text[:1000]
        )
        if company_id:
            print(f"✓ Saved to database (ID: {company_id})")
    
    return data


def batch_process(urls: List[str], scrape_method: str = "auto",
                 output_file: Optional[str] = None):
    """
    Process multiple URLs
    
    Args:
        urls: List of URLs
        scrape_method: Scraping method
        output_file: Save results to JSON file
    """
    print(f"\n{'='*60}")
    print(f"Batch Processing {len(urls)} URLs")
    print(f"{'='*60}")
    
    results = []
    successful = 0
    failed = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url}")
        
        try:
            data = scrape_and_extract(url, scrape_method, save_to_db=True)
            if data:
                results.append(data)
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Batch Processing Complete")
    print(f"{'='*60}")
    print(f"Successful: {successful}/{len(urls)}")
    print(f"Failed: {failed}/{len(urls)}")
    
    # Save results
    if output_file and results:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✓ Results saved to: {output_file}")
    
    return results


def search_database(query: str, search_type: str = "industry"):
    """
    Search saved companies
    
    Args:
        query: Search term
        search_type: "industry" or "name"
    """
    db = CompanyDatabase()
    
    if search_type == "industry":
        results = db.search_by_industry(query)
    else:
        # Name search
        results = db.get_all_companies()
        results = [c for c in results if query.lower() in str(c.get('company_name', '')).lower()]
    
    if results:
        print(f"\n{'='*60}")
        print(f"Search Results for '{query}' ({len(results)} found)")
        print(f"{'='*60}")
        
        for company in results:
            print(f"\n• {company.get('company_name')}")
            print(f"  Industry: {company.get('industry', 'N/A')}")
            print(f"  Email: {company.get('email', 'N/A')}")
            print(f"  Phone: {company.get('phone', 'N/A')}")
            print(f"  Confidence: {company.get('confidence', 0):.0%}")
    else:
        print(f"No results found for '{query}'")


def show_database_stats():
    """Display database statistics"""
    db = CompanyDatabase()
    stats = db.get_stats()
    
    print(f"\n{'='*60}")
    print(f"Database Statistics")
    print(f"{'='*60}")
    print(f"Total Companies: {stats.get('total_companies', 0)}")
    print(f"Average Confidence: {stats.get('avg_confidence', 0):.2f}")
    print(f"Unique Industries: {stats.get('unique_industries', 0)}")
    
    if stats.get('top_industries'):
        print(f"\nTop Industries:")
        for industry, count in stats['top_industries'].items():
            print(f"  • {industry}: {count}")
    
    print(f"{'='*60}")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Company Information Extraction System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from single URL
  python main.py --url https://example.com
  
  # Process multiple URLs from file
  python main.py --batch urls.txt --output results.json
  
  # Search by industry
  python main.py --search "Technology" --search-type industry
  
  # Show statistics
  python main.py --stats
  
  # Start Streamlit UI
  streamlit run ui/app.py
        """
    )
    
    # Single URL processing
    parser.add_argument(
        "--url",
        type=str,
        help="Website URL to process"
    )
    
    # Batch processing
    parser.add_argument(
        "--batch",
        type=str,
        help="File containing list of URLs (one per line)"
    )
    
    # Scraping method
    parser.add_argument(
        "--method",
        choices=["auto", "static", "playwright"],
        default="auto",
        help="Scraping method (default: auto)"
    )
    
    # Output file
    parser.add_argument(
        "--output",
        type=str,
        help="Save results to JSON file"
    )
    
    # Database search
    parser.add_argument(
        "--search",
        type=str,
        help="Search saved companies"
    )
    
    parser.add_argument(
        "--search-type",
        choices=["industry", "name"],
        default="industry",
        help="Type of search (default: industry)"
    )
    
    # Database stats
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show database statistics"
    )
    
    # Config
    parser.add_argument(
        "--config",
        action="store_true",
        help="Show current configuration"
    )
    
    args = parser.parse_args()
    
    # Show configuration
    if args.config:
        print("\nConfiguration:")
        print(f"  LLM Backend: {config.LLM_BACKEND}")
        print(f"  Model: {config.OLLAMA_MODEL}")
        print(f"  Temperature: {config.LLM_TEMPERATURE}")
        print(f"  Scrape Method: {config.DEFAULT_SCRAPE_METHOD}")
        print(f"  Database: {config.DATABASE_PATH}")
        return
    
    # Show stats
    if args.stats:
        show_database_stats()
        return
    
    # Search database
    if args.search:
        search_database(args.search, args.search_type)
        return
    
    # Single URL
    if args.url:
        data = scrape_and_extract(args.url, args.method, save_to_db=True)
        
        if args.output and data:
            with open(args.output, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n✓ Results saved to: {args.output}")
        return
    
    # Batch processing
    if args.batch:
        urls = []
        try:
            with open(args.batch, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ File not found: {args.batch}")
            return
        
        if urls:
            batch_process(urls, args.method, args.output)
        return
    
    # No action specified
    parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
