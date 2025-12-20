"""
Web Scraper Module
Handles both static HTML (requests + BeautifulSoup) and JS-heavy pages (Playwright)
"""

import requests
from bs4 import BeautifulSoup
import asyncio
import logging
from typing import Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # Disable SSL verification (safe for public scraping; fixes Windows cert issues)
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _normalize_url(self, url: str) -> str:
        """
        Ensure the URL has a scheme; default to https:// if missing.
        """
        if not url:
            return url
        lowered = url.strip().lower()
        if lowered.startswith("http://") or lowered.startswith("https://"):
            return url.strip()
        logger.info(f"No scheme detected for '{url}'. Prepending https://")
        return f"https://{url.strip()}"

    def scrape_static_html(self, url: str) -> Optional[str]:
        """
        Scrape static HTML content using requests + BeautifulSoup
        
        Args:
            url: Target URL
            
        Returns:
            Cleaned text content or None if failed
        """
        try:
            url = self._normalize_url(url)
            logger.info(f"Scraping static HTML: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            logger.info(f"Successfully scraped {len(text)} characters")
            return text
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None

    async def scrape_js_heavy_page(self, url: str) -> Optional[str]:
        """
        Scrape JavaScript-heavy pages using Playwright
        
        Args:
            url: Target URL
            
        Returns:
            Cleaned text content or None if failed
        """
        try:
            # Lazy import to avoid hard dependency when Playwright/browsers aren't installed
            try:
                from playwright.async_api import async_playwright
            except Exception as imp_err:
                logger.warning(f"Playwright not available: {imp_err}. Skipping JS scraping.")
                return None

            url = self._normalize_url(url)
            logger.info(f"Scraping JS-heavy page: {url}")
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(url, wait_until='networkidle', timeout=self.timeout * 1000)
                
                # Wait for content to load
                await page.wait_for_load_state('domcontentloaded')
                
                # Get page content
                content = await page.content()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove script and style
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                await browser.close()
                
                logger.info(f"Successfully scraped {len(text)} characters with Playwright")
                return text
                
        except Exception as e:
            logger.error(f"Error scraping JS-heavy page {url}: {str(e)}")
            return None

    def auto_scrape(self, url: str) -> Optional[str]:
        """
        Smart scraper - tries static first, then JS-heavy
        
        Args:
            url: Target URL
            
        Returns:
            Cleaned text content
        """
        # Try static scraping first (faster)
        text = self.scrape_static_html(url)
        
        if text and len(text) > 100:
            return text
        
        # If static fails or returns little content, try Playwright
        logger.info("Switching to Playwright for JS content")
        try:
            text = asyncio.run(self.scrape_js_heavy_page(url))
        except Exception as e:
            logger.warning(f"Playwright path failed: {e}. Returning None.")
            text = None
        
        return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks for LLM processing
    
    Args:
        text: Input text
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks


if __name__ == "__main__":
    # Test the scraper
    scraper = WebScraper()
    
    # Test with a sample URL
    test_url = "https://www.example.com"
    result = scraper.auto_scrape(test_url)
    
    if result:
        chunks = chunk_text(result)
        print(f"Successfully scraped and chunked into {len(chunks)} pieces")
        print(f"First chunk: {chunks[0][:200]}...")
    else:
        print("Scraping failed")
