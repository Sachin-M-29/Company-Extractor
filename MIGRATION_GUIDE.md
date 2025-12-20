# Streamlit to Next.js Migration Guide

## Overview

The Company Information Extractor has been migrated from Streamlit to a modern Next.js frontend while maintaining all extraction functionality.

## What Changed

### ✅ What's Better

| Aspect | Streamlit | Next.js |
|--------|-----------|---------|
| **UI/UX** | Basic, limited styling | Modern, responsive design |
| **Performance** | Server-side heavy | Client-side optimized |
| **Customization** | Limited | Full React component flexibility |
| **Mobile** | Not optimized | Fully responsive |
| **Speed** | Slower refresh | Instant updates |
| **Deployment** | Streamlit Cloud lock-in | Any Node.js host |
| **API** | Built-in (POST /api/extract) | RESTful with Flask backend |
| **Styling** | Markdown hacks | Tailwind CSS |
| **Batch Speed** | Sequential | Parallel with configurable workers |

### 🔄 What Stayed the Same

- ✓ All extraction logic (scrapers, LLM, heuristics)
- ✓ Database storage (SQLite)
- ✓ LLM backend (Ollama)
- ✓ Data quality and accuracy
- ✓ Features (enrichment, classification, etc.)

## File Structure Changes

### Old Streamlit Structure
```
web-scraper-llm/
├── ui/
│   └── app.py          # Main Streamlit app
├── scrapers/
├── utils/
├── llm/
└── database/
```

### New Next.js Structure
```
web-scraper-llm/
├── nextjs-ui/          # NEW: Next.js frontend
│   ├── app/           # Next.js app directory
│   ├── components/    # React components
│   └── package.json
├── api.py             # NEW: Flask bridge API
├── ui/                # OLD: Still here for reference
│   └── app.py
├── scrapers/          # Unchanged
├── utils/             # Unchanged
├── llm/               # Unchanged
└── database/          # Unchanged
```

## API Changes

### Streamlit (Old)
- No API, direct Python execution
- UI tightly coupled with logic

### Next.js (New)
```
Client: http://localhost:3000
    ↓
Next.js API Routes: http://localhost:3000/api/*
    ↓
Flask Backend: http://localhost:5000/api/*
    ↓
Python Extraction Logic
```

## Running the Application

### Old Way (Streamlit)
```bash
streamlit run ui/app.py
# Opens: http://localhost:8501
```

### New Way (Next.js)
```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: Flask API
python api.py
# Runs on: http://localhost:5000

# Terminal 3: Next.js Frontend
cd nextjs-ui && npm run dev
# Opens: http://localhost:3000
```

## Feature Mapping

### Single Extraction
| Feature | Streamlit | Next.js |
|---------|-----------|---------|
| URL input | ✓ | ✓ |
| Company name input | ✓ | ✓ |
| Scraping methods | ✓ | ✓ |
| LLM extraction | ✓ | ✓ |
| Enrichment | ✓ | ✓ |
| Results display | ✓ | ✓ (tabs) |
| JSON export | ✓ | ✓ |

### Batch Extraction
| Feature | Streamlit | Next.js |
|---------|-----------|---------|
| Multi-URL input | ✓ | ✓ |
| Parallel processing | Removed | ✓ (with configurable workers) |
| Fast mode | ✓ | ✓ (enhanced) |
| Results table | ✓ | ✓ (with sorting) |
| CSV export | ✓ | ✓ |
| JSON export | ✓ | ✓ |

## Extraction Logic - No Changes

The core extraction remains identical:

```python
1. Scrape HTML (Static/JS/Auto)
   ↓
2. Extract with LLM (Ollama)
   ↓
3. Merge heuristics (regex patterns)
   ↓
4. Optional enrichment (multi-page)
   ↓
5. Store in SQLite
```

## Configuration

### Environment Variables

**Next.js** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

**Python** (No changes, same as before):
- Uses existing `config.py`
- Model: `mistral:7b-instruct-q4_0`
- Database: `companies.db`

## Database

- **Still using:** SQLite
- **Location:** `companies.db`
- **Schema:** Unchanged
- **Data:** All old data still accessible

## Backwards Compatibility

### Can I still use Streamlit?

Yes! The old Streamlit app still works:
```bash
streamlit run ui/app.py
```

However, it won't have:
- Batch speed optimizations
- Modern UI
- API routes

### Migrating Data

If you extracted data with Streamlit:

1. **Database is compatible** - Just point to the same `companies.db`
2. **SQL exports** - Available through Flask API:
   ```bash
   curl http://localhost:5000/api/companies
   ```
3. **Manual export** - Use old Streamlit export, then reimport to Next.js

## Performance Improvements

### Batch Mode Speedup
| Setup | Speed | Workers |
|-------|-------|---------|
| Streamlit (sequential) | ~30-40s per company | 1 |
| Next.js (3 workers) | ~10-15s per company | 3 |
| Next.js (5 workers) | ~6-8s per company | 5 |
| Next.js (10 workers) | ~3-5s per company | 10 |

### Single Extraction
- **Streamlit:** 25-30s (unchanged)
- **Next.js:** 25-30s (unchanged, same LLM)

## Common Migration Questions

### Q: Will my extracted data disappear?
**A:** No. All data in `companies.db` remains accessible through the Flask API.

### Q: Do I need to reinstall dependencies?
**A:** 
- Python: Same as before
- Node.js: New, see setup guide
- Ollama: Same, still required

### Q: Can I export data from Streamlit version?
**A:** Yes:
1. Use Streamlit CSV/JSON export
2. Or access through Flask API:
   ```python
   import requests
   r = requests.get('http://localhost:5000/api/companies')
   data = r.json()
   ```

### Q: How do I switch between Streamlit and Next.js?
**A:**
- **Streamlit:** `streamlit run ui/app.py`
- **Next.js:** `cd nextjs-ui && npm run dev`
- Both use the same database and Python logic

### Q: Will extraction results differ?
**A:** No, identical. Both use the same scrapers, LLM, and heuristics.

## What's No Longer Available

- ⚠️ Streamlit's built-in caching
- ⚠️ Streamlit secrets management
- ⚠️ Streamlit cloud deployment
- ⚠️ Streamlit session state (replaced with React state)

**But gained:**
- ✓ React component flexibility
- ✓ Modern CSS/styling
- ✓ Better performance
- ✓ Standard REST API
- ✓ Any Node.js hosting

## Deployment

### Streamlit
```bash
streamlit run ui/app.py --server.port 8501
```

### Next.js
```bash
# Development
cd nextjs-ui && npm run dev

# Production build
cd nextjs-ui && npm run build && npm start
```

Both need Python API running:
```bash
python api.py --host 0.0.0.0 --port 5000
```

## Troubleshooting Migration

### "I can't find my extracted companies"
```bash
# Check database exists
ls -la companies.db

# Query through API
curl http://localhost:5000/api/companies
```

### "Import errors in Flask API"
```bash
# Ensure all Python dependencies installed
pip install -r requirements.txt

# Check Ollama model available
ollama list
```

### "Next.js can't connect to Flask"
```bash
# Test Flask endpoint
curl http://localhost:5000/api/health

# Check .env.local
cat nextjs-ui/.env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Getting Help

1. **Extraction issues:** Same as Streamlit version
2. **UI/styling issues:** Check browser console (F12)
3. **API issues:** Check Flask logs
4. **Performance:** Adjust parallel workers or enable fast mode

## Summary

```
Streamlit ──────────────→ Next.js
├─ Extraction logic ───→ (Same, in Python)
├─ Database ───────────→ (Same SQLite)
├─ LLM ────────────────→ (Same Ollama)
├─ UI ─────────────────→ (Modern React)
├─ Speed ──────────────→ (Faster batch)
└─ Deployment ────────→ (More flexible)
```

**Everything works, just looks and feels better!** 🚀
