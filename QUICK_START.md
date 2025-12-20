# Quick Start Guide - Next.js UI

Get started with the Company Information Extractor in 5 minutes!

## Prerequisites

- **Node.js 18+** - [Download](https://nodejs.org)
- **Python 3.8+** - [Download](https://python.org)
- **Ollama** - [Download](https://ollama.ai)

Verify installations:
```bash
node --version    # v18 or higher
python --version  # 3.8 or higher
ollama --version  # Running
```

## Step 1: Install Dependencies

### Option A: Auto Setup (Recommended)

**Windows:**
```bash
cd c:\projects\data\web-scraper-llm
setup-nextjs.bat
```

**macOS/Linux:**
```bash
cd /path/to/web-scraper-llm
bash setup-nextjs.sh
```

### Option B: Manual Setup

```bash
# Python dependencies
pip install flask flask-cors requests beautifulsoup4 playwright
python -m playwright install

# Next.js dependencies
cd nextjs-ui
npm install
cd ..
```

## Step 2: Start Services

Open 3 terminal windows:

### Terminal 1: Ollama
```bash
ollama serve
```
Wait for: `Listening on 127.0.0.1:11434`

### Terminal 2: Flask API
```bash
python api.py
```
You should see: `* Running on http://0.0.0.0:5000`

### Terminal 3: Next.js Frontend
```bash
cd nextjs-ui
npm run dev
```
You should see: `▲ Next.js ... Local: http://localhost:3000`

## Step 3: Open Browser

Visit: **http://localhost:3000**

You should see the Company Extractor UI with:
- Header navigation
- Search form on the left
- Results area on the right

## Step 4: Try It Out

### Test 1: Extract One Company

1. Keep "URL" selected
2. Enter: `google.com`
3. Click "Extract Info"
4. Wait ~30 seconds for results
5. See results in tabs
6. Click "Export" to download JSON

### Test 2: Batch Extract

1. Click "Batch Extraction" tab
2. Enter:
   ```
   google.com
   github.com
   ```
3. Set "Parallel workers: 2"
4. Click "Extract Batch"
5. Wait for results
6. Download as CSV or JSON

### Test 3: Check Database

Open terminal and query:
```bash
curl http://localhost:5000/api/companies
```

See all extracted companies in JSON format.

## Common Issues & Fixes

### "API not responding"

```bash
# Check Flask is running
curl http://localhost:5000/api/health

# Response should be:
# {"status":"ok","message":"Company Extractor API is running"}

# If not, restart Flask:
# Kill: Ctrl+C in Flask terminal
# Restart: python api.py
```

### "LLM extraction failed"

```bash
# Make sure Ollama is running
ollama serve

# Check model exists
ollama list
# Should show: mistral:7b-instruct-q4_0

# If missing, download it:
ollama pull mistral:7b-instruct-q4_0
```

### "Can't connect to http://localhost:3000"

```bash
# Make sure Next.js started properly
# Check "npm run dev" output in terminal
# Try: http://localhost:3000
# If still fails, restart: Ctrl+C then npm run dev
```

### Extraction is slow

This is normal! Mistral 7B takes 20-30 seconds per company.

To speed up:
- Use **Fast Mode** in batch extraction
- Disable **Enrichment**
- Increase **Parallel Workers** (if CPU allows)

## Configuration Quick Reference

| Setting | Purpose | Recommended |
|---------|---------|-------------|
| **Scraping Method** | How to get webpage content | Static HTML Only |
| **Timeout** | Max seconds per request | 10 |
| **Enrichment** | Extract people/products | Off (for speed) |
| **Fast Mode** | Skip slow operations | On |
| **Workers** | Parallel threads | 3-5 |

## File Locations

- **Next.js UI**: `nextjs-ui/` directory
- **Flask API**: `api.py` file
- **Database**: `companies.db` file
- **Config**: `nextjs-ui/.env.local`

## Next Steps

1. ✅ Completed: Extract your first company
2. 📊 Try batch extraction with 5-10 URLs
3. 💾 Check `companies.db` for stored data
4. 📥 Download results as CSV
5. 📖 Read `NEXTJS_README.md` for full features

## Performance Tips

| Task | Time | Notes |
|------|------|-------|
| Single company | 25-30s | LLM processing |
| 10 companies (1 worker) | 4-5 min | Sequential |
| 10 companies (5 workers) | 30-50s | Parallel |
| 100 companies (5 workers) | 5-8 min | Scales linearly |

## Keyboard Shortcuts

- `Ctrl+C` - Stop server (any terminal)
- `F12` - Open browser developer tools
- `Ctrl+L` - Clear URL bar

## Need Help?

1. **Check logs:**
   - Flask terminal: Shows API errors
   - Browser console: F12 → Console tab
   - Next.js terminal: Shows build errors

2. **Check troubleshooting:**
   - `NEXTJS_README.md` - Full troubleshooting section
   - `MIGRATION_GUIDE.md` - Migration issues

3. **Test services:**
   ```bash
   # Test Ollama
   curl http://localhost:11434/api/tags
   
   # Test Flask API
   curl http://localhost:5000/api/health
   
   # Test Next.js
   curl http://localhost:3000
   ```

## What to Expect

### Successful Extraction
```json
{
  "company_name": "Google LLC",
  "website": "https://www.google.com",
  "industry": "Information Technology",
  "email": "contact@google.com",
  "linkedin": "https://linkedin.com/company/google",
  "products": ["Search", "Gmail", "Maps"],
  "confidence": 0.95
}
```

### Batch Results Table
- Shows all companies extracted
- Sortable by name or confidence
- Download buttons for CSV/JSON
- Failure count displayed

## Clean Up

To stop all services:

```bash
# Terminal 1: Press Ctrl+C
ollama serve

# Terminal 2: Press Ctrl+C
python api.py

# Terminal 3: Press Ctrl+C
npm run dev
```

## Advanced: Production Deploy

See `NEXTJS_README.md` for:
- Building for production
- Deploying to cloud
- Network access setup

## Summary Checklist

- [ ] Installed Node.js, Python, Ollama
- [ ] Ran setup script
- [ ] Started Ollama (`ollama serve`)
- [ ] Started Flask (`python api.py`)
- [ ] Started Next.js (`cd nextjs-ui && npm run dev`)
- [ ] Opened http://localhost:3000
- [ ] Extracted a test company
- [ ] Downloaded results as JSON

🎉 **You're ready to go!**

Questions? See:
- `NEXTJS_README.md` - Full documentation
- `MIGRATION_GUIDE.md` - Detailed setup
- Browser console (F12) - Error messages
