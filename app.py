"""
Hugging Face Spaces App for Company Extractor
FastAPI backend served on Hugging Face Spaces
"""

import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.scraper import WebScraper, chunk_text
from utils.resolve import resolve_company_website
from utils.heuristics import extract_all as heuristic_extract
from utils.enrich import enrich_company_details
from llm.hf_extractor import HFExtractor
from database.db import CompanyDatabase

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Company Extractor API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = CompanyDatabase()
extractor = HFExtractor(
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    use_gpu=True
)

logger.info("Company Extractor API initialized with Mistral 7B")


# Pydantic models
class ExtractionRequest(BaseModel):
    input: str
    input_type: str = "url"
    scrape_method: str = "Static HTML Only"
    timeout: int = 10
    enable_enrich: bool = False


class ExtractedCompany(BaseModel):
    company_name: str
    website: str
    description: Optional[str] = None
    industry: Optional[str] = None
    confidence: float = 0.0


# Routes
@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Company Extractor API is running",
        "backend": "Hugging Face Spaces",
        "model": "Mistral 7B Instruct"
    }


@app.post("/api/extract")
async def extract_single(request: ExtractionRequest):
    """Extract company information from single URL or company name"""
    try:
        input_text = request.input.strip()
        
        if not input_text:
            raise HTTPException(status_code=400, detail="Input is required")
        
        # Resolve company website
        if request.input_type == "company_name":
            print(f"[API] Resolving company: {input_text}")
            company_url = resolve_company_website(input_text)
            if not company_url:
                raise HTTPException(status_code=404, detail="Could not find company website")
        else:
            company_url = input_text
            if not company_url.startswith("http"):
                company_url = f"https://{company_url}"
        
        print(f"[API] Extracting: {input_text} (type: {request.input_type})")
        print(f"[API] Website: {company_url}")
        
        # Scrape website
        scraper = WebScraper(timeout=request.timeout)
        
        if request.scrape_method == "Static HTML Only":
            scraped_text = scraper.scrape_static_html(company_url)
        elif request.scrape_method == "Auto (Smart)":
            try:
                scraped_text = scraper.auto_scrape(company_url)
            except Exception:
                scraper.close()
                scraped_text = scraper.scrape_static_html(company_url)
        else:
            scraped_text = scraper.scrape_static_html(company_url)
        
        scraper.close()
        
        if not scraped_text:
            raise HTTPException(status_code=400, detail="Failed to scrape website content")
        
        print(f"[API] Scraped {len(scraped_text)} characters, extracting with LLM...")
        
        # Extract with LLM
        chunks = chunk_text(scraped_text, chunk_size=500, overlap=50)
        text_to_extract = chunks[0] if chunks else scraped_text
        
        extracted_data = extractor.extract_from_text(text_to_extract, company_url)
        
        if not extracted_data:
            raise HTTPException(status_code=500, detail="Failed to extract company information")
        
        print(f"[API] Extraction complete, merging heuristics...")
        
        # Merge with heuristic extraction
        heuristic_data = heuristic_extract(scraped_text, company_url)
        merged_data = {**heuristic_data, **extracted_data}
        
        # Enrich if requested
        if request.enable_enrich:
            print(f"[API] Enriching details...")
            merged_data = enrich_company_details(merged_data)
        
        # Store in database
        db.insert_company(merged_data)
        print(f"[API] Success: {merged_data.get('company_name')}")
        
        return {
            "success": True,
            "data": merged_data,
            "scrape_method": request.scrape_method
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/batch-extract")
async def extract_batch(urls: List[str], background_tasks: BackgroundTasks):
    """Extract from multiple URLs"""
    if not urls or len(urls) == 0:
        raise HTTPException(status_code=400, detail="URLs list is required")
    
    results = []
    errors = []
    
    for url in urls:
        try:
            request_data = ExtractionRequest(input=url, input_type="url")
            response = await extract_single(request_data)
            results.append({
                "url": url,
                "success": True,
                "data": response["data"]
            })
        except Exception as e:
            errors.append({
                "url": url,
                "success": False,
                "error": str(e)
            })
    
    return {
        "total": len(urls),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }


@app.get("/api/companies")
async def get_companies(limit: int = 50, offset: int = 0):
    """Get extracted companies from database"""
    try:
        companies = db.get_companies(limit=limit, offset=offset)
        
        avg_confidence = 0
        industries = set()
        
        if companies:
            total_confidence = sum(float(c.get('confidence', 0)) for c in companies)
            avg_confidence = total_confidence / len(companies)
            
            for c in companies:
                if c.get('industry'):
                    industries.add(c.get('industry'))
        
        print(f"[API] Returning {len(companies)} companies from database")
        
        return {
            'companies': companies,
            'stats': {
                'total': len(companies),
                'avg_confidence': round(avg_confidence, 2),
                'industries_found': len(industries)
            }
        }
    except Exception as e:
        print(f"[API] Error fetching companies: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Company Extractor API",
        "version": "1.0.0",
        "description": "Extract company information from websites using Mistral 7B",
        "backend": "Hugging Face Spaces",
        "endpoints": {
            "health": "/api/health",
            "extract": "/api/extract (POST)",
            "batch_extract": "/api/batch-extract (POST)",
            "companies": "/api/companies (GET)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
