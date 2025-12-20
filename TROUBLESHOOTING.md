# Troubleshooting Guide

## Extraction Timeout Issue

If you see "timeout of 20000ms exceeded" or similar errors, this is likely due to the Ollama LLM taking too long to process.

### Why It Happens:
1. **LLM Processing**: Mistral 7B model takes 20-60 seconds to extract information from text
2. **Enrichment Mode**: Additional web scraping adds 30-120 seconds
3. **Combined Total**: Single extraction with enrichment can take 60-180 seconds

### Solutions:

#### Option 1: Disable Enrichment (Recommended for first test)
- Uncheck "Enable Enrichment" in the UI
- This reduces time from 60-180s to 20-60s

#### Option 2: Use Faster Timeout Settings
- Set Timeout to 30+ seconds instead of 10
- Allows Flask more time to process

#### Option 3: Upgrade LLM Model (For advanced users)
- Switch to `mistral:7b-q4_0` (smaller model, faster)
- Or use `neural-chat` for faster processing

#### Option 4: Enable Fast Mode for Batch
- Use batch extraction with Fast Mode enabled
- Set workers to 5-10 for parallel processing
- Processes multiple companies simultaneously

## What's Happening Under the Hood:

```
POST /api/extract
├─ Scrape website (2-5 seconds)
├─ Extract with Ollama LLM (20-60 seconds)
│  └─ This is the slow step!
├─ Merge with heuristics (1-2 seconds)
└─ Optional: Enrich with multi-page crawl (30-120 seconds)
│  └─ This is VERY slow!
```

## Debug Mode:

Check Flask terminal logs for `[API]` messages showing extraction progress:
- `[API] Extracting: {company}`
- `[API] Scraping: {url}`
- `[API] Scraped X characters, extracting with LLM...`
- `[API] Success: {company_name}`

## Verify Ollama is Running:

```bash
# Check if Ollama server is running
ollama list

# If model not loaded, pull it:
ollama pull mistral:7b-instruct-q4_0

# Start Ollama if not running:
ollama serve
```

## Test Extraction Directly:

```bash
# Test without enrichment
curl -X POST http://localhost:5000/api/extract \
  -H "Content-Type: application/json" \
  -d '{
    "input": "google.com",
    "input_type": "url",
    "scrape_method": "Static HTML Only",
    "timeout": 30,
    "enable_enrich": false
  }'
```

Expected time: 20-30 seconds, then JSON response.

## Performance Tips:

1. **Disable enrichment** unless you need company details like address, people
2. **Use batch mode** with 5 workers to process multiple companies in parallel
3. **Set timeout to 30+** seconds to allow LLM time
4. **Run on fast machine** - LLM processing is CPU-intensive
5. **Keep Ollama model loaded** - First run after long idle takes longer
