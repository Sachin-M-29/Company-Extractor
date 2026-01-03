# Deploy to Hugging Face Spaces - Complete Guide

## Overview

Your Company Extractor will run 24/7 on Hugging Face Spaces with:
- ✅ No credit card required
- ✅ Free forever ($0/month)
- ✅ Mistral 7B model (same quality as before)
- ✅ Same API endpoints (no frontend changes)
- ✅ 24/7 uptime

**Total setup time:** 15 minutes

---

## Step 1: Sign Up for Hugging Face (2 minutes)

1. **Go to:** https://huggingface.co
2. **Click "Sign up"**
3. **Use GitHub signup** (recommended)
4. **Verify your email**

---

## Step 2: Create Hugging Face Space

1. **Go to:** https://huggingface.co/spaces
2. **Click "Create new Space"**
3. **Fill in details:**
   - **Space name:** `company-extractor`
   - **Owner:** Your username
   - **Space type:** `Docker`
   - **Visibility:** `Public` (recommended) or `Private`

4. **Click "Create Space"**

HF will create an empty Docker space.

---

## Step 3: Connect Your GitHub Repository

In your HF Space:

1. **Click "Files" → "Add file"**
2. **Click "Upload files"**

Or better - **use GitHub sync:**

1. **Space Settings → Repository URL**
2. **Paste:** `https://github.com/Sachin-M-29/Company-Extractor/tree/huggingface-spaces`
3. **Save**

HF will automatically pull and deploy your code!

---

## Step 4: Create Docker Configuration

The space needs a `Dockerfile`. It's already in your repo!

If it doesn't show, create one:

**File: `Dockerfile`**
```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## Step 5: Create HF Spaces App

**File: `app.py`** (create in repo root)

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from scrapers.scraper import WebScraper, chunk_text
from utils.resolve import resolve_company_website
from utils.heuristics import extract_all as heuristic_extract
from utils.enrich import enrich_company_details
from llm.cli_extractor import CLIExtractor
from database.db import CompanyDatabase

app = FastAPI(title="Company Extractor API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
db = CompanyDatabase()

# LLM Extractor
try:
    llm_extractor = CLIExtractor(model="mistralai/Mistral-7B-Instruct-v0.1", gpu_device=0)
except Exception as e:
    logging.warning(f"LLM extractor not available: {e}")
    llm_extractor = None


class ExtractRequest(BaseModel):
    input: str
    input_type: str = "url"
    scrape_method: str = "Static HTML Only"
    timeout: int = 10
    enable_enrich: bool = False


@app.get("/api/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "Company Extractor API is running"}


@app.post("/api/extract")
async def extract_single(request: ExtractRequest):
    """Extract company information from single URL or company name"""
    try:
        input_text = request.input.strip()
        input_type = request.input_type
        scrape_method = request.scrape_method
        timeout = request.timeout
        enable_enrich = request.enable_enrich

        if not input_text:
            raise HTTPException(status_code=400, detail="Input is required")

        # Resolve company website if name is provided
        if input_type == "company_name":
            resolved_urls = resolve_company_website(input_text)
            if not resolved_urls:
                raise HTTPException(status_code=404, detail=f"Could not resolve website for {input_text}")
            url = resolved_urls[0]
        else:
            url = input_text

        # Scrape website
        scraper = WebScraper(method=scrape_method, timeout=timeout)
        scraped_html = scraper.scrape(url)
        
        if not scraped_html:
            raise HTTPException(status_code=400, detail="Failed to scrape website")

        # Extract with LLM
        llm_data = None
        if llm_extractor:
            llm_data = llm_extractor.extract_from_text(scraped_html, url)

        # Heuristic extraction
        heuristic_data = heuristic_extract(scraped_html, url)

        # Merge results
        merged_data = llm_data or heuristic_data or {}
        
        # Enrichment
        if enable_enrich:
            merged_data = enrich_company_details(merged_data)

        # Save to database
        if merged_data.get("company_name"):
            db.insert_company(merged_data)

        return {
            "success": True,
            "data": merged_data,
            "source": "llm" if llm_data else "heuristic"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
```

---

## Step 6: Update requirements.txt

Add these lines to `requirements.txt`:

```
fastapi==0.104.1
uvicorn==0.24.0
transformers==4.35.0
torch==2.1.0
```

---

## Step 7: Wait for Deployment

HF will automatically:
1. Pull your repository
2. Build the Docker image (takes 5-10 minutes)
3. Start the FastAPI server
4. Provide a public URL

**Watch the "Logs" tab for progress.**

---

## Step 8: Get Your Backend URL

Once deployment completes (green checkmark ✓):

1. **At the top of the space**, you'll see a URL like:
   ```
   https://sachin-m-29-company-extractor.hf.space/
   ```

2. **Test it:**
   ```
   https://sachin-m-29-company-extractor.hf.space/api/health
   ```

   Should return:
   ```json
   {"status": "ok", "message": "Company Extractor API is running"}
   ```

**Save this URL** - you'll need it for Vercel!

---

## Step 9: Deploy Frontend to Vercel

In PowerShell:

```powershell
cd C:\projects\data\web-scraper-llm\nextjs-ui

npm install -g vercel
vercel login
vercel
```

Answer prompts as before, then:

```powershell
vercel env add NEXT_PUBLIC_PYTHON_API production
```

**Paste your HF Spaces URL:**
```
https://sachin-m-29-company-extractor.hf.space
```

Deploy to production:
```powershell
vercel --prod
```

---

## Step 10: Test Your Live App

1. **Visit your Vercel URL**
2. **Test extraction** with a website URL
3. **Verify** data appears correctly

---

## FAQ

### Model takes too long to load

**Expected on first run:** Mistral 7B downloads on first request (~1-2 min)

**After first run:** Fast inference (30-60 sec per extraction)

### GPU not available in HF Spaces

**HF Spaces free tier is CPU-only.** Model still works, just slower.

**Upgrade to GPU** (optional, paid):
- In Space Settings
- Select GPU tier
- Costs ~$0.50/hour

### Running out of memory

HF Spaces provides 16GB, which is enough for Mistral 7B.

If issues:
- Use smaller quantization: `mistralai/Mistral-7B-Instruct-v0.2`
- Or use DistilMistral (smaller model)

### API returns 502 error

Space is still starting. Wait 2-3 minutes and try again.

### Frontend can't connect

1. Verify `NEXT_PUBLIC_PYTHON_API` is set in Vercel
2. Test HF API directly: `https://your-space.hf.space/api/health`
3. Check browser console for CORS errors

---

## Monitoring

### Check HF Space Logs

1. Go to your HF Space
2. Click "Logs" tab
3. See real-time server output

### Monitor Usage

1. HF Space Settings → "Usage"
2. See CPU/memory/time used

### Disable Space (to save resources)

1. Settings → "Status" → "Pause"
2. Restarts anytime with fresh build

---

## Updates

### Update Backend Code

```powershell
cd C:\projects\data\web-scraper-llm

# Make changes
git add .
git commit -m "Update extraction"
git push origin huggingface-spaces
```

HF automatically rebuilds and redeploys (5-10 min)!

### Update Frontend

```powershell
cd nextjs-ui
vercel --prod
```

---

## Cost Summary

| Component | Cost |
|-----------|------|
| HF Spaces (CPU) | **$0/month** |
| Vercel Frontend | **$0/month** |
| Ollama Model | **$0/month** |
| **Total** | **$0/month** |

**24/7 Uptime:** ✅ Yes  
**No Credit Card:** ✅ Yes  
**Same Quality:** ✅ Yes

---

## Your Deployment is Complete! 🎉

### URLs

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-username-company-extractor.hf.space`
- **GitHub:** `https://github.com/Sachin-M-29/Company-Extractor` (branch: `huggingface-spaces`)

### What's Next?

1. Share your live app!
2. Test with various websites
3. Gather feedback
4. Iterate and improve

Enjoy your free, 24/7 company extractor! 🚀
