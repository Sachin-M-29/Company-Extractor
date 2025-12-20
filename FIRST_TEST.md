# Quick Test Guide

## First Time Setup Complete! ✅

Your system is now running:
- **Next.js UI**: http://localhost:3001
- **Flask API**: http://localhost:5000
- **Ollama LLM**: Running locally

## First Extraction Test

### ⚠️ IMPORTANT: Disable Enrichment for First Test

When you first test the system:

1. Go to http://localhost:3001
2. Enter: `google.com` (reliable website)
3. **UNCHECK** "Enable Enrichment" ⬅️ KEY STEP!
4. Click "Extract Info"
5. Wait 20-60 seconds (Ollama is analyzing)

### Expected Results:

✅ Should succeed with:
```json
{
  "company_name": "Google",
  "website": "https://google.com",
  "short_description": "...",
  ...
}
```

### If It Still Fails:

Check Flask logs for `[API]` messages:
```
[API] Extracting: google.com
[API] Scraping: https://google.com
[API] Scraped X characters, extracting with LLM...
[API] Success: Google
```

## Understanding Extraction Time

| Setting | Time | Speed | Notes |
|---------|------|-------|-------|
| No Enrichment | 20-60s | ⚡ Fast | Best for first test |
| With Enrichment | 60-180s | 🐢 Slow | Crawls multiple pages |
| Batch (5 workers) | 5-15s/company | ⚡⚡ Very fast | Parallel processing |

## Troubleshooting

### "timeout of 20000ms exceeded"
**Problem**: Extraction taking longer than expected
**Solution**: 
- Uncheck "Enable Enrichment" 
- Increase timeout slider to 30+ seconds
- Or wait longer (Ollama might be slow on first run)

### "Extraction failed"
**Problem**: Flask API not responding
**Solution**:
```bash
# Check Flask is running:
curl http://localhost:5000/api/health

# Check Ollama:
ollama list
```

### Very Slow Processing
**Problem**: Ollama model taking 60+ seconds
**Solution**: This is normal for Mistral 7B on CPU
- First run is slowest (model loading)
- Subsequent runs are faster (model cached)
- Use smaller model: `ollama pull neural-chat:7b`

## Next Steps

1. ✅ Test single extraction (no enrichment)
2. Try batch extraction with 5 companies
3. Enable enrichment for important companies
4. Check database: `companies.db` in web-scraper-llm folder

## Performance Tips

```javascript
// Fast mode (default)
- No enrichment
- Static HTML only
- Result: 20-60 seconds per company

// Balanced mode  
- No enrichment
- Auto smart scraping
- Result: 30-90 seconds per company

// Comprehensive mode
- With enrichment
- Auto scraping
- Result: 60-180 seconds per company
// BUT: Do 5 companies in parallel = 2-3 minutes for 5 companies!
```

## Batch Extraction (Much Faster!)

For 10+ companies, use Batch Extraction:
1. Switch to "Batch Extraction" tab
2. Paste 10 URLs (one per line)
3. Set Fast Mode ON
4. Set Workers: 5
5. Results: All 10 in ~2-3 minutes!

Vs. single extraction: 10 × 60 seconds = 10 minutes

## System is Working Correctly! 🎉

If you see extraction results in the UI, everything is working.
The system is designed to take 20-60 seconds per extraction
because Ollama LLM processing is CPU-intensive.

This is normal and expected.
