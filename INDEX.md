# 📖 Documentation Index

Complete guide to the Company Information Extractor with Next.js UI.

## 🚀 Getting Started (Read These First)

### For First-Time Users
1. **[QUICK_START.md](QUICK_START.md)** ⭐ Start here!
   - 5-minute setup
   - Quick testing
   - Common issues

2. **[NEXTJS_README.md](NEXTJS_README.md)** - Complete guide
   - Feature overview
   - Full setup instructions
   - Configuration options
   - API reference
   - Troubleshooting

### For Streamlit Users
3. **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Streamlit → Next.js
   - What changed
   - What stayed the same
   - Data preservation
   - Migration steps

---

## 📚 Detailed Documentation

### Understanding the System
- **[NEXTJS_COMPLETE.md](NEXTJS_COMPLETE.md)** - Complete technical overview
  - What was built (file listing)
  - Architecture diagram
  - Feature matrix
  - Performance metrics
  - Technology stack

- **[NEXTJS_MIGRATION_SUMMARY.md](NEXTJS_MIGRATION_SUMMARY.md)** - Project summary
  - What was created
  - Design decisions
  - Testing checklist
  - Quick reference

### Specific Guides
- **[nextjs-ui/README.md](nextjs-ui/README.md)** - Frontend setup
  - Installation
  - Development
  - Building for production
  - Component overview

---

## 🎯 Quick Reference

### Installation
```bash
# Windows
setup-nextjs.bat

# macOS/Linux
bash setup-nextjs.sh
```

### Running Services
```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: Flask API
python api.py

# Terminal 3: Next.js Frontend
cd nextjs-ui && npm run dev
```

### Access
- **Frontend**: http://localhost:3000
- **Flask API**: http://localhost:5000
- **Ollama**: http://localhost:11434

---

## 📁 File Structure

```
web-scraper-llm/
├── 📖 Documentation
│   ├── QUICK_START.md              ← Start here!
│   ├── NEXTJS_README.md            ← Full guide
│   ├── MIGRATION_GUIDE.md          ← For Streamlit users
│   ├── NEXTJS_COMPLETE.md          ← Technical details
│   ├── NEXTJS_MIGRATION_SUMMARY.md ← Project summary
│   ├── README.md                   ← Original docs
│   └── INDEX.md                    ← This file
│
├── 🎨 Next.js Frontend (nextjs-ui/)
│   ├── app/                        ← Pages & components
│   │   ├── page.tsx               ← Main page
│   │   ├── about/page.tsx         ← About page
│   │   ├── analytics/page.tsx     ← Analytics page
│   │   ├── api/                   ← API routes
│   │   └── globals.css            ← Styling
│   ├── components/                 ← React components
│   ├── package.json               ← Dependencies
│   └── README.md                  ← Frontend guide
│
├── 🐍 Python Backend
│   ├── api.py                     ← Flask API bridge
│   ├── scrapers/                  ← Web scraping
│   ├── utils/                     ← Utilities
│   ├── llm/                       ← LLM integration
│   └── database/                  ← Data persistence
│
├── 🔧 Setup Scripts
│   ├── setup-nextjs.bat           ← Windows setup
│   └── setup-nextjs.sh            ← macOS/Linux setup
│
└── 📊 Original UI (deprecated)
    └── ui/app.py                  ← Old Streamlit app
```

---

## 🎓 Documentation by Topic

### Getting Running
1. [QUICK_START.md](QUICK_START.md) - Installation & first run
2. [NEXTJS_README.md](NEXTJS_README.md#setup) - Detailed setup
3. [nextjs-ui/README.md](nextjs-ui/README.md) - Frontend setup

### Using the Application
1. [QUICK_START.md](QUICK_START.md#step-4-try-it-out) - Basic usage
2. [NEXTJS_README.md](NEXTJS_README.md#usage-guide) - Full usage guide
3. [NEXTJS_README.md](NEXTJS_README.md#troubleshooting) - Troubleshooting

### Understanding Architecture
1. [NEXTJS_COMPLETE.md](NEXTJS_COMPLETE.md#-architecture) - Architecture overview
2. [NEXTJS_README.md](NEXTJS_README.md#architecture) - System design
3. [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#file-structure-changes) - File layout

### Configuration & Customization
1. [NEXTJS_README.md](NEXTJS_README.md#configuration) - All settings
2. [nextjs-ui/README.md](nextjs-ui/README.md#development) - Development setup
3. [NEXTJS_README.md](NEXTJS_README.md#api-endpoints) - API reference

### For Developers
1. [NEXTJS_COMPLETE.md](NEXTJS_COMPLETE.md#-technology-stack) - Tech stack
2. [nextjs-ui/README.md](nextjs-ui/README.md#components) - Components guide
3. [NEXTJS_README.md](NEXTJS_README.md#styling) - Styling info

---

## 🔍 Searching for Information

### "How do I..."

**...get started?**
→ [QUICK_START.md](QUICK_START.md)

**...install dependencies?**
→ [QUICK_START.md - Step 1](QUICK_START.md#step-1-install-dependencies)

**...start the services?**
→ [QUICK_START.md - Step 2](QUICK_START.md#step-2-start-services)

**...extract one company?**
→ [QUICK_START.md - Step 4](QUICK_START.md#step-4-try-it-out)

**...extract multiple companies?**
→ [NEXTJS_README.md - Batch Mode](NEXTJS_README.md#batch-processing)

**...fix a problem?**
→ [QUICK_START.md - Issues](QUICK_START.md#common-issues--fixes)

**...export results?**
→ [NEXTJS_README.md - Export](NEXTJS_README.md#export-options)

**...migrate from Streamlit?**
→ [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

**...configure settings?**
→ [NEXTJS_README.md - Configuration](NEXTJS_README.md#configuration)

**...deploy to production?**
→ [NEXTJS_README.md - Deployment](NEXTJS_README.md#deployment)

**...understand the architecture?**
→ [NEXTJS_COMPLETE.md - Architecture](NEXTJS_COMPLETE.md#-architecture)

---

## 📊 Quick Stats

| Aspect | Details |
|--------|---------|
| **Setup Time** | 5-10 minutes |
| **First Run** | ~30 seconds |
| **Single Extraction** | 25-30 seconds |
| **Batch Speed** | 3-4x faster (with parallel processing) |
| **Files Created** | 25+ files |
| **Components** | 5 React components |
| **Pages** | 3 pages |
| **API Endpoints** | 3 REST endpoints |
| **Terminals Needed** | 3 (Ollama, Flask, Next.js) |
| **Browser URL** | http://localhost:3000 |

---

## ✨ Feature Checklist

### Single Extraction
- [x] URL input with auto-formatting
- [x] Company name input with resolution
- [x] Configurable scraping method
- [x] Timeout setting
- [x] Enrichment toggle
- [x] Results in 6 tabs
- [x] JSON export

### Batch Extraction
- [x] Multi-URL input
- [x] Parallel processing (1-10 workers)
- [x] Fast mode optimization
- [x] Results table with sorting
- [x] CSV export
- [x] JSON export
- [x] Failure tracking

### Data Extracted
- [x] Company info (name, website, industry, sector)
- [x] Contact (email, phone, address)
- [x] Social media (11 platforms)
- [x] People (team members, titles, profiles)
- [x] Products & services
- [x] Certifications (40+ patterns)
- [x] Industry classification
- [x] Confidence scores

---

## 🎯 Common Paths

### Path A: "I want to use the app now"
1. Read: [QUICK_START.md](QUICK_START.md)
2. Run: setup script
3. Start: 3 services
4. Visit: http://localhost:3000

### Path B: "I'm coming from Streamlit"
1. Read: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
2. Check: [What's Different](MIGRATION_GUIDE.md#what-changed)
3. Follow: [QUICK_START.md](QUICK_START.md)

### Path C: "I want to understand the system"
1. Read: [NEXTJS_COMPLETE.md](NEXTJS_COMPLETE.md)
2. Review: Architecture section
3. Check: Technology stack

### Path D: "I'm a developer"
1. Read: [nextjs-ui/README.md](nextjs-ui/README.md)
2. Check: Components guide
3. Review: API endpoints

### Path E: "I need to troubleshoot"
1. Check: [QUICK_START.md - Issues](QUICK_START.md#common-issues--fixes)
2. Review: [NEXTJS_README.md - Troubleshooting](NEXTJS_README.md#troubleshooting)
3. Check: Browser console (F12)

---

## 📱 Documentation Versions

| Format | Version | Status |
|--------|---------|--------|
| Markdown | Latest | Current |
| HTML | - | Not generated |
| PDF | - | Available on request |

All documentation is in Markdown format. View in:
- GitHub
- VS Code
- Any Markdown viewer
- Browser (via GitHub)

---

## 🔗 Cross References

**Getting Started:**
- QUICK_START.md ← → NEXTJS_README.md (detailed)
- QUICK_START.md ← → MIGRATION_GUIDE.md (for Streamlit users)

**Understanding:**
- NEXTJS_COMPLETE.md ← → NEXTJS_MIGRATION_SUMMARY.md
- NEXTJS_README.md ← → nextjs-ui/README.md

**Troubleshooting:**
- QUICK_START.md ← → NEXTJS_README.md
- MIGRATION_GUIDE.md ← → Common Issues section

---

## 📞 Support Channels

1. **Browser Console** - F12 → Console tab
   - Shows React/JavaScript errors
   - API response logging

2. **Flask Terminal** - Where you ran `python api.py`
   - Shows API errors
   - Request logging

3. **Next.js Terminal** - Where you ran `npm run dev`
   - Shows build errors
   - Compilation warnings

4. **Documentation** - See relevant guide above

5. **Logs** - Check:
   - `companies.db` - Database integrity
   - Terminal output - Recent errors

---

## 🎉 Summary

| Document | Best For | Read Time |
|----------|----------|-----------|
| **QUICK_START.md** | Getting running fast | 5 min |
| **NEXTJS_README.md** | Complete reference | 15 min |
| **MIGRATION_GUIDE.md** | Streamlit users | 10 min |
| **NEXTJS_COMPLETE.md** | Understanding system | 20 min |
| **NEXTJS_MIGRATION_SUMMARY.md** | Technical overview | 10 min |

**Recommended reading order:**
1. QUICK_START.md (get it running)
2. NEXTJS_README.md (understand features)
3. NEXTJS_COMPLETE.md (if curious about details)

---

## 📝 Document Metadata

- **Last Updated**: December 20, 2025
- **Version**: 1.0 (Initial Release)
- **Status**: Complete & Production-Ready
- **Pages**: 6 main documents + 2 README files
- **Total Content**: 40+ pages
- **Languages**: English
- **Format**: Markdown

---

**Happy extracting!** 🚀

For questions, check the relevant documentation above or review browser console (F12) for detailed error messages.
