# Company Information Extractor - Next.js UI

Modern Next.js frontend for the Company Information Extractor system. Replaces the Streamlit UI with a professional web interface.

## Features

- ✨ **Modern UI** - Built with Next.js, React, and Tailwind CSS
- 🚀 **Single & Batch Extraction** - Extract from one or multiple companies simultaneously
- 📊 **Parallel Processing** - Configurable worker count for faster batch operations
- ⚡ **Fast Mode** - Optimized settings for rapid batch extraction
- 📥 **Multiple Exports** - Download results as JSON or CSV
- 🎯 **Rich Results** - Company info, contacts, social, products, team, certifications
- 🔌 **API-driven** - Connects to Python Flask backend

## Architecture

```
nextjs-ui/ (This folder)
├── app/                    # Next.js app directory
│   ├── page.tsx           # Main page
│   ├── layout.tsx         # Root layout
│   ├── globals.css        # Global styles
│   └── api/               # API routes (proxy to Flask)
│       ├── extract/       # Single extraction endpoint
│       ├── batch-extract/ # Batch extraction endpoint
│       └── export/        # Export endpoint
├── components/            # React components
│   ├── company-search.tsx # Search form
│   ├── company-list.tsx   # Batch results table
│   ├── results-tabs.tsx   # Single result tabs
│   └── navigation.tsx     # Top navbar
└── public/               # Static assets

../api.py                 # Flask backend (Python)
```

## Setup

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.8+ (for Flask backend)
- Ollama running locally (`ollama serve`)

### 1. Install Next.js Dependencies

```bash
cd nextjs-ui
npm install
# or
yarn install
```

### 2. Install Python Dependencies

```bash
# From project root
pip install flask flask-cors axios
```

### 3. Start the Flask Backend

```bash
python api.py
```

The API will run on `http://localhost:5000`

### 4. Start the Next.js Development Server

```bash
cd nextjs-ui
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

### Single Extraction

1. Select "URL" or "Company Name" input type
2. Enter a website URL or company name
3. Choose scraping method (Static HTML, Auto, or Playwright)
4. Enable enrichment if needed (people, products, services)
5. Click "Extract Info"
6. View results in tabs or export as JSON

### Batch Extraction

1. Click "Batch Extraction" tab
2. Enter multiple URLs (one per line, comma, or space-separated)
3. Configure:
   - Scraping method
   - Fast mode (limits pages and timeout)
   - Parallel workers (1-10, default 3)
4. Click "Extract Batch"
5. Results appear in table format
6. Download as JSON or CSV

## Configuration

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Flask Backend Settings

Edit `api.py`:

```python
# Model selection
extractor = CLIExtractor(model='mistral:7b-instruct-q4_0')

# Other models available:
# - phi3:3.8b-mini-4k-instruct-q4_0
# - orca2:7b-q4
# - neural-chat:7b-v3-q4
```

## Development

### Build

```bash
npm run build
```

### Production

```bash
npm start
```

## API Endpoints

All endpoints proxy requests to the Flask backend at `http://localhost:5000`.

### POST /api/extract

Single company extraction.

```json
{
  "input": "example.com",
  "input_type": "url",
  "scrape_method": "Static HTML Only",
  "timeout": 10,
  "enable_enrich": false
}
```

### POST /api/batch-extract

Batch company extraction.

```json
{
  "urls": ["example.com", "google.com"],
  "scrape_method": "Static HTML Only",
  "timeout": 10,
  "fast_mode": true,
  "max_workers": 3
}
```

### GET /api/health

Check API health.

## Styling

Uses Tailwind CSS v3. Configuration in `tailwind.config.js`.

Custom animations and utilities in `app/globals.css`.

## Components

### CompanySearch
Form for single/batch extraction with settings

### ResultsTabs
Tabbed display of extracted company data

### CompanyList
Table view of batch results with sorting and export

### Navigation
Header with navigation links

## Troubleshooting

### Flask API not responding

```bash
# Check Flask is running
curl http://localhost:5000/api/health

# Restart Flask
python api.py
```

### Next.js build errors

```bash
# Clear cache
rm -rf .next
npm run build
```

### CORS errors

Make sure Flask is running with CORS enabled:

```python
from flask_cors import CORS
CORS(app)
```

## Performance

- **Single extraction**: 20-30 seconds (depends on Ollama model)
- **Batch mode**: 3-5 URLs in parallel at 1-2 sec each per worker
- **Fast mode**: Reduces enrichment pages from 6 to 2, uses 5s timeout

## Future Enhancements

- [ ] Analytics dashboard with extracted data insights
- [ ] Graph visualization of company relationships
- [ ] Advanced filtering and search
- [ ] Scheduled batch jobs
- [ ] Admin dashboard
- [ ] User authentication
- [ ] Data validation and quality scoring

## License

MIT

## Support

For issues or questions, check the main project README.
