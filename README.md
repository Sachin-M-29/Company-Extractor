# Company Information Extraction System

A complete pipeline for scraping company websites and extracting structured information using AI/LLM.

## Architecture

```
URL/Company Name
      ↓
Requests + BeautifulSoup (static HTML)
Playwright (JavaScript-heavy pages)
      ↓
Clean HTML → Text
      ↓
Text Chunking (500 token chunks with overlap)
      ↓
LLM Processing (Mistral/Phi-3/Ollama)
      ↓
Structured JSON Output
      ↓
SQLite Database + FAISS Vector Store
      ↓
Streamlit Web UI
```

## System Requirements

- **GPU**: NVIDIA RTX 2050+ (2GB VRAM minimum)
- **CPU**: Intel i5 or equivalent
- **RAM**: 8GB minimum
- **CUDA**: 11.8 or higher
- **Python**: 3.10+

## Hardware Optimization

### GPU Model Selection

For your **RTX 2050 + CUDA 11.8**, we recommend:

1. **Mistral-7B-Instruct (Q4)** ⭐ **RECOMMENDED**
   - Size: 3.3GB (Q4 quantization)
   - Speed: ~20-30 tokens/sec
   - Quality: Excellent
   - Command: `ollama pull mistral:7b-instruct-q4_0`

2. **Phi-3-mini (Q4)** - If memory is tight
   - Size: 1.5GB (Q4 quantization)
   - Speed: ~40-60 tokens/sec
   - Quality: Good
   - Command: `ollama pull phi3:3.8b-mini-4k-instruct-q4_0`

3. **Orca-2-7B (Q4)** - Best reasoning
   - Size: 3.3GB (Q4 quantization)
   - Speed: ~15-25 tokens/sec
   - Quality: Very Good
   - Command: `ollama pull orca2:7b-q4`

See [GPU_MODEL_RECOMMENDATION.md](GPU_MODEL_RECOMMENDATION.md) for detailed comparison.

## Installation

### 1. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install Ollama

Download from https://ollama.ai and install.

### 3. Install LLM Model

```bash
# Download and quantize model (first time takes 5-10 minutes)
ollama pull mistral:7b-instruct-q4_0

# Start Ollama server (keep running)
ollama serve
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 5. Optional: Install Playwright for JS-heavy pages

```bash
playwright install
```

## Project Structure

```
web-scraper-llm/
├── scrapers/
│   └── scraper.py          # BeautifulSoup + Playwright scrapers
├── llm/
│   └── extractor.py        # LLM extraction with system prompt
├── database/
│   └── db.py               # SQLite + FAISS storage
├── ui/
│   └── app.py              # Streamlit web interface
├── requirements.txt        # Python dependencies
├── GPU_MODEL_RECOMMENDATION.md
└── README.md
```

## Usage

### Option 1: Streamlit Web UI (Recommended)

```bash
# Make sure Ollama is running in another terminal
ollama serve

# In another terminal, run Streamlit
streamlit run ui/app.py

# Open browser to http://localhost:8501
```

### Option 2: Python Script

```python
from scrapers.scraper import WebScraper, chunk_text
from llm.extractor import LLMExtractor
from database.db import CompanyDatabase
import json

# Initialize components
scraper = WebScraper()
extractor = LLMExtractor()
db = CompanyDatabase()

# Scrape
url = "https://example.com"
text = scraper.auto_scrape(url)

# Extract
chunks = chunk_text(text)
data = extractor.extract_from_text(chunks[0], url)

# Store
db.insert_company(data, url, "static", len(text), 2.5)

# Print results
print(json.dumps(data, indent=2))
```

### Option 3: Batch Processing

```python
from scrapers.scraper import WebScraper, chunk_text
from llm.extractor import LLMExtractor
from database.db import CompanyDatabase

urls = [
    "https://company1.com",
    "https://company2.com",
    "https://company3.com",
]

scraper = WebScraper()
extractor = LLMExtractor()
db = CompanyDatabase()

for url in urls:
    # Scrape
    text = scraper.auto_scrape(url)
    if not text:
        continue
    
    # Extract
    from scrapers.scraper import chunk_text
    chunks = chunk_text(text)
    data = extractor.extract_from_text(chunks[0], url)
    
    # Store
    if data:
        db.insert_company(data, url, "auto", len(text), 0)
        print(f"✓ {data.get('company_name')}")
```

## Extracted Information Format

The system extracts and returns structured JSON:

```json
{
  "company_name": "TechCorp Inc.",
  "industry": "Artificial Intelligence",
  "products": ["AI Analytics", "ML Platform"],
  "email": "sales@techcorp.ai",
  "phone": "+1-415-555-0100",
  "address": "San Francisco, CA",
  "website": "https://techcorp.ai",
  "description": "Leading provider of AI solutions for enterprises",
  "confidence": 0.85,
  "extraction_notes": "All main fields successfully extracted"
}
```

## LLM System Prompt

The system uses this prompt for extraction:

```
You are an information extraction system for company websites.

EXTRACTION RULES:
1. Extract ONLY information that exists in the text
2. If data is not found, return null (NOT empty string, NOT "N/A")
3. Output MUST be valid JSON
4. Do NOT hallucinate or invent information
5. Be precise and concise

FIELDS TO EXTRACT:
- company_name: Official company name
- industry: Industry/sector
- products: List of products or services
- email: Primary contact email
- phone: Phone number
- address: Physical address
- website: The website URL
- description: Brief 1-2 sentence description
```

## Performance Tips

### 1. Optimize for Your GPU

- Use 4-bit quantization (reduces VRAM by 4x)
- Keep batch size to 1
- Use smaller chunk sizes (500 tokens)

### 2. Faster Scraping

- Use static HTML scraping for simple sites
- Only use Playwright when needed (JS content)
- Set appropriate timeout values

### 3. Batch Processing

```python
# Process multiple URLs efficiently
texts_with_urls = [
    (text1, "https://url1.com"),
    (text2, "https://url2.com"),
]

results = extractor.batch_extract(texts_with_urls)
```

### 4. Memory Management

```bash
# Monitor VRAM usage
nvidia-smi watch -n 1

# Limit to 1 GPU
CUDA_VISIBLE_DEVICES=0 streamlit run ui/app.py
```

## Troubleshooting

### Error: "Cannot connect to Ollama server"

```bash
# Make sure Ollama is running in another terminal
ollama serve

# Or start as background service (Windows)
ollama start
```

### Error: "CUDA out of memory"

1. Use smaller model: `phi3:3.8b-mini-4k-instruct-q4_0`
2. Use more aggressive quantization (Q2 instead of Q4)
3. Reduce chunk size to 250 tokens
4. Close other GPU-consuming applications

### Playwright browser not found

```bash
# Download required browsers
playwright install chromium
```

### Low extraction confidence

- Ensure text contains relevant company information
- Check that LLM model is properly loaded
- Verify system prompt is not being truncated

## Database

### SQLite Storage

Companies are stored in local SQLite database with:
- Basic info (name, industry, products, etc.)
- Contact information
- Processing metadata
- Creation/update timestamps

### FAISS Vector Store (Optional)

For semantic search capabilities:
```python
from database.db import FAISSVectorStore

vector_store = FAISSVectorStore()
# Add embeddings and search by similarity
```

## API Integration

### REST API Example (using FastAPI)

```python
from fastapi import FastAPI
from scrapers.scraper import WebScraper, chunk_text
from llm.extractor import LLMExtractor
from database.db import CompanyDatabase

app = FastAPI()

@app.post("/extract")
async def extract_company(url: str):
    scraper = WebScraper()
    extractor = LLMExtractor()
    db = CompanyDatabase()
    
    text = scraper.auto_scrape(url)
    chunks = chunk_text(text)
    data = extractor.extract_from_text(chunks[0], url)
    
    db.insert_company(data, url, "auto", len(text), 0)
    return data
```

## Next Steps

1. **Fine-tune the system prompt** for your specific extraction needs
2. **Add more data sources** (LinkedIn, CrunchBase APIs, etc.)
3. **Implement validation** using secondary sources
4. **Build search interface** with semantic similarity
5. **Add scheduling** for periodic re-scraping
6. **Deploy to cloud** (AWS, Azure, GCP)

## Performance Benchmarks

On RTX 2050 with Mistral-7B-Q4:

| Operation | Time | Memory |
|-----------|------|--------|
| Scrape static HTML | 1-3s | 200MB |
| Playwright scrape | 5-8s | 800MB |
| LLM extraction | 3-5s | 3.5GB |
| Database insert | <100ms | 50MB |
| **Total** | **9-16s** | **Peak 3.5GB** |

## License

MIT License - Feel free to modify and use for your projects

## Support

For issues or questions:
1. Check [GPU_MODEL_RECOMMENDATION.md](GPU_MODEL_RECOMMENDATION.md)
2. Review error logs in terminal
3. Verify Ollama model is loaded correctly
4. Check database integrity with `sqlite3 companies.db`

## Citation

If you use this system in research, please cite:

```
Web Scraper + LLM Information Extraction System
For company data extraction and structuring
Built with: Ollama, Mistral, SQLite, Streamlit
```
