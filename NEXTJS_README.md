# Company Information Extractor - Next.js UI Edition

A modern web application for extracting and organizing company data using web scraping + AI. This is the Next.js version that replaces the previous Streamlit UI.

## 🌟 Features

- **✨ Modern Web UI** - Built with Next.js, React, and Tailwind CSS
- **🔍 Single Extraction** - Extract company details from a single URL
- **📊 Batch Processing** - Process hundreds of companies with parallel workers
- **⚡ Fast Mode** - Optimized for rapid extraction
- **🤖 AI-Powered** - Uses local Ollama LLM (no internet required)
- **📥 Multiple Exports** - JSON, CSV formats
- **💾 Data Persistence** - SQLite database
- **🔧 Configurable** - Scraping methods, timeouts, enrichment options

## 📋 What Gets Extracted

- **Company Info**: Name, website, industry, sector, description
- **Contact Details**: Email, phone, address
- **Social Media**: LinkedIn, Facebook, Twitter, Instagram, YouTube, Blog
- **People**: Team members with titles and profiles
- **Products & Services**: What the company offers
- **Certifications**: ISO, SOC2, GDPR, HIPAA, etc.
- **Classification**: Industry, sub-industry, confidence score

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** ([download](https://nodejs.org))
- **Python 3.8+** ([download](https://python.org))
- **Ollama** running locally ([install](https://ollama.ai))

### 1. Clone/Open Project

```bash
cd web-scraper-llm
```

### 2. Run Setup Script

**On Windows:**
```bash
setup-nextjs.bat
```

**On macOS/Linux:**
```bash
bash setup-nextjs.sh
```

Or manually install:

```bash
# Python dependencies
pip install flask flask-cors requests beautifulsoup4 playwright
python -m playwright install

# Next.js dependencies
cd nextjs-ui
npm install
cd ..
```

### 3. Start Services

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Flask API:**
```bash
python api.py
# API runs at http://localhost:5000
```

**Terminal 3 - Next.js Frontend:**
```bash
cd nextjs-ui
npm run dev
# UI runs at http://localhost:3000
```

### 4. Open Browser

Visit [http://localhost:3000](http://localhost:3000)

## 📚 Usage Guide

### Single Company Extraction

1. Select **"Single Extraction"** tab
2. Choose input type: **URL** or **Company Name**
3. Enter website (e.g., `example.com`) or company name
4. Configure options:
   - **Scraping Method**: Static HTML, Auto, or Playwright
   - **Timeout**: 5-60 seconds
   - **Enrichment**: Enable for people/products/services (slower)
5. Click **"Extract Info"**
6. View results in tabs or **export as JSON**

### Batch Company Extraction

1. Select **"Batch Extraction"** tab
2. Paste multiple URLs (one per line, or comma/space separated):
   ```
   example.com
   google.com
   microsoft.com
   ```
3. Configure options:
   - **Scraping Method**: Choose extraction strategy
   - **Fast Mode**: ⚡ Limits to 2 pages and 5s timeout (recommended)
   - **Parallel Workers**: 1-10 (3-5 recommended)
4. Click **"Extract Batch"**
5. Results appear in table
6. **Download as JSON or CSV**

### Export Options

- **JSON**: Full data structure with all fields
- **CSV**: Simplified table format (name, website, industry, confidence)

## 🏗️ Architecture

```
web-scraper-llm/
├── nextjs-ui/                 # Next.js Frontend
│   ├── app/                   # Next.js app directory
│   │   ├── page.tsx           # Home page
│   │   ├── about/             # About page
│   │   ├── analytics/         # Analytics page
│   │   ├── api/               # API routes
│   │   │   ├── extract/       # Single extraction
│   │   │   ├── batch-extract/ # Batch extraction
│   │   │   └── export/        # Export handler
│   │   └── globals.css        # Tailwind CSS
│   ├── components/            # React components
│   │   ├── company-search.tsx # Search form
│   │   ├── company-list.tsx   # Batch results table
│   │   ├── results-tabs.tsx   # Results display
│   │   └── navigation.tsx     # Header navigation
│   └── package.json           # Dependencies
│
├── api.py                     # Flask Backend
├── scrapers/                  # Web scraping modules
├── utils/                     # Utility functions
├── llm/                       # LLM integration
└── database/                  # Database layer
```

## 🔌 API Reference

### Single Extraction

**POST** `/api/extract`

```json
{
  "input": "example.com",
  "input_type": "url",
  "scrape_method": "Static HTML Only",
  "timeout": 10,
  "enable_enrich": false
}
```

**Response:**
```json
{
  "company_name": "Example Inc.",
  "website": "https://example.com",
  "industry": "Technology",
  "email": "contact@example.com",
  "linkedin": "https://linkedin.com/company/...",
  "products": [...],
  "team": [...],
  "certifications": [...]
}
```

### Batch Extraction

**POST** `/api/batch-extract`

```json
{
  "urls": ["example.com", "google.com"],
  "scrape_method": "Static HTML Only",
  "timeout": 10,
  "fast_mode": true,
  "max_workers": 3
}
```

**Response:**
```json
{
  "results": [...],
  "failures": [],
  "success_count": 2,
  "failure_count": 0,
  "total_count": 2
}
```

## ⚙️ Configuration

### Scraping Methods

1. **Static HTML Only** (Recommended)
   - Fastest, no JavaScript rendering
   - Works for most websites
   - 2-5 second typical time

2. **Auto (Smart)**
   - Tries static first, falls back to Playwright
   - Best for JS-heavy sites
   - 5-10 seconds typical

3. **Playwright Only**
   - Full browser automation
   - Handles complex interactions
   - 10-30 seconds typical

### Fast Mode (Batch)

When enabled:
- ⚡ Limits enrichment to 2 pages (instead of 6)
- ⚡ Timeout reduced to 5 seconds (fail faster)
- ⚡ Skips slow operations
- ✓ Still extracts core info accurately

## 🛠️ Troubleshooting

### "API not responding"
```bash
# Check Flask is running
curl http://localhost:5000/api/health

# Restart Flask
python api.py
```

### "LLM extraction failed"
```bash
# Check Ollama is running
ollama serve

# Verify model is available
ollama list
# Should see: mistral:7b-instruct-q4_0
```

### Next.js build errors
```bash
# Clear cache and rebuild
cd nextjs-ui
rm -rf .next
npm run build
```

### CORS errors
- Ensure Flask has CORS enabled (it does by default in api.py)
- Check NEXT_PUBLIC_API_URL is correct

### Slow extraction
- Enable **Fast Mode** for faster results
- Increase **Parallel Workers** (if CPU allows)
- Disable **Enrichment** if not needed
- Use **Static HTML Only** scraping

## 📊 Performance

| Scenario | Time | Speed | Notes |
|----------|------|-------|-------|
| Single company (Basic) | 20-30s | Standard | LLM processing time |
| Single company (Enriched) | 30-60s | Standard | Includes multi-page crawl |
| Batch 10 companies (3 workers, fast) | 30-50s | 3-5 sec/company | Parallel processing |
| Batch 100 companies (5 workers, fast) | 5-8 min | ~3 sec/company | Scales linearly |

**Factors affecting speed:**
- LLM model (Mistral 7B is standard)
- Website size and complexity
- Network speed
- CPU/GPU resources
- Parallel workers count

## 🔒 Privacy & Security

- ✓ **All processing local** - No data sent to external services
- ✓ **Ollama offline** - LLM runs on your machine
- ✓ **SQLite database** - Data stored locally
- ✓ **No API keys** - No authentication needed
- ✓ **Open source** - Full transparency

## 📦 What's Included

- Web scraping with fallback methods
- Ollama LLM integration
- 40+ regex patterns for certification detection
- 11 social media platform detection
- Industry/sector classification
- Email and phone extraction
- SQLite data persistence
- Parallel batch processing
- JSON/CSV export
- Modern responsive UI

## 🚀 Deployment

### Local Network Access

To access from other machines on your network:

1. In `nextjs-ui/.env.local`, change:
```env
NEXT_PUBLIC_API_URL=http://YOUR_IP:5000
```

2. Start Flask with:
```bash
python api.py --host 0.0.0.0
```

3. Access from other machines:
```
http://YOUR_IP:3000
```

### Production Deployment

See `nextjs-ui/README.md` for production build instructions.

## 📝 CLI Usage (Legacy)

For the original Streamlit interface:
```bash
streamlit run ui/app.py
```

For batch extraction script:
```bash
python batch_extract.py urls.txt
```

## 🎯 Roadmap

- [x] Next.js modern UI
- [x] Batch extraction with parallelization
- [x] Export to CSV/JSON
- [x] Fast mode optimization
- [ ] Analytics dashboard
- [ ] Graph visualization
- [ ] Advanced filtering
- [ ] Scheduled jobs
- [ ] Data validation scoring
- [ ] Web-based admin panel

## 📄 License

MIT

## 🤝 Contributing

Bug reports and feature requests welcome! Please see main README for details.

## 📞 Support

- Check the **About** page in the app
- Review logs in browser console (F12)
- Check Flask output in terminal
- See troubleshooting section above

## 🎉 Credits

Built with:
- [Next.js](https://nextjs.org)
- [React](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Flask](https://flask.palletsprojects.com)
- [Ollama](https://ollama.ai)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup)
