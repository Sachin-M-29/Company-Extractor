# Quick Reference: Export & Analytics

## 🎯 Three Main Pages

### 1. 🏠 Home Page (localhost:3000)
**Extract company information**
- Single Extraction: Enter 1 company
- Batch Extraction: Paste multiple URLs
- Options: Scraping method, timeout, enrichment

### 2. 📊 Analytics Page (localhost:3000/analytics)
**View & download extracted data**
- Live statistics (total companies, confidence, industries)
- Company data table (shows 50, download for all)
- CSV export button
- JSON export button

### 3ℹ️ About Page (localhost:3000/about)
**System information & documentation**

---

## 📥 Download Your Data

### CSV Download
1. Click "Download as CSV" button on Analytics page
2. File opens in Excel automatically
3. All 1000+ companies included
4. Ready to analyze, pivot, sort

### JSON Download
1. Click "Download as JSON" button on Analytics page
2. File saved as `companies.json`
3. Use in Python, Node.js, or any tool
4. Perfect for APIs and integrations

---

## 📈 Analytics Page Features

### Statistics Cards (Top)
- **Total Companies**: How many you've extracted
- **Average Confidence**: Data quality score (0-100%)
- **Industries Found**: Unique industry categories

### Company Table (Below)
Shows first 50 companies with:
- Company name
- Website (clickable)
- Industry category
- Confidence % (green badge)
- Email address
- Phone number

*Download CSV/JSON to see remaining companies*

---

## 🔄 Workflow Example

```
1. Go to http://localhost:3000
   ↓
2. Paste 10 company URLs
   ↓
3. Set Fast Mode: ON
   ↓
4. Set Workers: 5
   ↓
5. Click "Extract Info"
   ↓
6. Wait 2-3 minutes (all 10 in parallel)
   ↓
7. Go to /analytics
   ↓
8. Click "Download as CSV"
   ↓
9. Open companies.csv in Excel
   ↓
10. Analyze, sort, filter, pivot!
```

---

## 💾 File Formats

### CSV (Excel Format)
```
company_name,website,industry,confidence,email,phone
Google,https://google.com,Technology,0.92,contact@google.com,
Amazon,https://amazon.com,Retail,0.91,support@amazon.com,
```

### JSON (Programmatic Format)
```json
[
  {
    "company_name": "Google",
    "website": "https://google.com",
    "industry": "Technology",
    "confidence": 0.92,
    "email": "contact@google.com",
    "phone": null
  }
]
```

---

## ⚙️ System Status

| Component | Status | URL |
|-----------|--------|-----|
| UI (Next.js) | ✅ Running | localhost:3000 |
| API (Flask) | ✅ Running | localhost:5000 |
| Database | ✅ Running | companies.db |
| Ollama (LLM) | ✅ Running | localhost:11434 |

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "No companies to download" | Extract 1+ companies first |
| Analytics page blank | Refresh page (F5) |
| CSV won't download | Check browser block pop-ups |
| Data not updating | Flask may need restart |
| Slow extraction | Use batch mode with workers=5 |

---

## 📝 Notes

- **Database**: All data saved in `companies.db` (SQLite)
- **Backup**: Download CSV/JSON regularly for backups
- **Limits**: Table shows first 50, downloads include all
- **Formats**: CSV for Excel, JSON for programming
- **Privacy**: All processing local, no cloud uploads

---

## 🚀 You're All Set!

Everything is installed and running. Start extracting companies and use the Analytics page to download your data!

**Next Steps:**
1. Extract some companies
2. Check Analytics page
3. Download as CSV or JSON
4. Use the data!
