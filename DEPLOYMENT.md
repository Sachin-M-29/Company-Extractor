# Git & Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### Step 1: Initialize Git Repository
```powershell
cd C:\projects\data\web-scraper-llm
git init
git add .
git commit -m "Initial commit: GPU-accelerated company extractor with Next.js frontend"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Create new repository: `company-extractor` (or your preferred name)
3. Copy the HTTPS URL (example: `https://github.com/yourusername/company-extractor.git`)

### Step 3: Push to GitHub
```powershell
git remote add origin https://github.com/yourusername/company-extractor.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy on Vercel
1. Go to https://vercel.com/new
2. Click "Import Project"
3. Paste your GitHub repository URL
4. Select: Next.js → Configure
5. Set environment variables:
   ```
   PYTHON_API=your-api-url.com/api
   NEXT_PUBLIC_PYTHON_API=your-api-url.com/api
   ```
6. Click "Deploy"

---

## 📁 Project Structure for Deployment

```
company-extractor/
├── nextjs-ui/                 # Next.js frontend (Vercel)
│   ├── app/
│   │   ├── page.tsx
│   │   ├── contact/page.tsx   # NEW
│   │   ├── about/page.tsx
│   │   ├── analytics/page.tsx
│   │   └── api/
│   ├── components/
│   ├── package.json
│   └── next.config.js
│
├── llm/                       # LLM extraction
│   ├── cli_extractor.py       # GPU-enabled
│   └── __init__.py
│
├── scrapers/                  # Web scraping
├── utils/                     # Utilities
├── database/                  # SQLite DB
│
├── api.py                     # Flask backend
├── config.py                  # Configuration
├── GPU_SETUP.md              # GPU guide
├── QUICKSTART.md             # Quick start
├── .gitignore                # Git ignore file
└── requirements.txt          # Python dependencies
```

---

## ⚙️ Files to Configure

### 1. Create `.gitignore` (in root):
```plaintext
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
.venv/
venv/
.env
.env.local

# Node
node_modules/
.next/
out/
dist/
npm-debug.log
yarn-debug.log

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Vercel
.vercel/
```

### 2. Create `vercel.json` (in root):
```json
{
  "buildCommand": "cd nextjs-ui && npm run build",
  "outputDirectory": "nextjs-ui/.next",
  "framework": "nextjs",
  "env": {
    "PYTHON_API": "@python_api_url",
    "NEXT_PUBLIC_PYTHON_API": "@next_public_python_api_url"
  }
}
```

### 3. Update `nextjs-ui/next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
      {
        protocol: 'http',
        hostname: '**',
      }
    ]
  },
  env: {
    PYTHON_API: process.env.PYTHON_API || 'http://127.0.0.1:5000',
    NEXT_PUBLIC_PYTHON_API: process.env.NEXT_PUBLIC_PYTHON_API || 'http://127.0.0.1:5000'
  }
}

module.exports = nextConfig
```

### 4. Create `requirements.txt` (in root):
```plaintext
Flask==3.0.0
Flask-CORS==4.0.0
requests==2.31.0
beautifulsoup4==4.12.0
selenium==4.15.0
playwright==1.40.0
python-dotenv==1.0.0
```

---

## 🔐 Important: Backend Deployment

**Note**: Vercel hosts only the Next.js frontend. Your Flask backend needs separate hosting:

### Option 1: Railway (Recommended)
1. Go to https://railway.app
2. Create new project → GitHub repo
3. Deploy Flask (api.py)
4. Get URL: `https://your-project.railway.app`
5. Set in Vercel env vars:
   ```
   PYTHON_API=https://your-project.railway.app
   NEXT_PUBLIC_PYTHON_API=https://your-project.railway.app
   ```

### Option 2: Render
1. Go to https://render.com
2. New → Web Service
3. Deploy Flask api.py
4. Set environment variables for GPU (if available)

### Option 3: PythonAnywhere
1. Go to https://pythonanywhere.com
2. Upload code and configure WSGI app
3. Get URL and add to Vercel env vars

---

## 📝 Git Workflow

### Initial Setup:
```powershell
# Create repo
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/company-extractor.git
git branch -M main
git push -u origin main
```

### After Making Changes:
```powershell
# Check what changed
git status

# Stage changes
git add .

# Commit
git commit -m "Your commit message"

# Push
git push origin main
```

### Common Commit Messages:
```
"Fix: GPU extraction not returning data"
"Feat: Add Contact Us page"
"Docs: Update GPU configuration guide"
"Refactor: Improve extraction prompt"
```

---

## 🎯 Vercel Deployment Checklist

- [ ] GitHub repository created
- [ ] Code pushed to main branch
- [ ] `vercel.json` configured
- [ ] `next.config.js` updated
- [ ] `.gitignore` created
- [ ] Environment variables set in Vercel dashboard
- [ ] Backend API deployed (Railway/Render/etc)
- [ ] Backend URL added to Vercel env vars
- [ ] Domain configured (optional)
- [ ] Custom domain CNAME set (optional)

---

## 🔍 After Deployment

### Test Your Deployment:
1. Visit: `https://your-project.vercel.app`
2. Test extraction with a company
3. Check browser console (F12) for errors
4. Monitor backend logs

### Common Issues:

**CORS Errors**: Backend API not accessible
- Check Flask-CORS configuration
- Verify backend URL in env vars
- Ensure backend is running

**Missing Data**: Fields are empty
- Check backend GPU configuration
- Verify Ollama model is available
- Review extraction logs

**Timeout Errors**: Extraction takes too long
- Increase timeout in environment
- Check GPU availability on backend
- Simplify extraction prompt if needed

---

## 📊 Environment Variables for Vercel

Go to Vercel Project Settings → Environment Variables:

```
PYTHON_API = https://your-backend.railway.app
NEXT_PUBLIC_PYTHON_API = https://your-backend.railway.app
```

**Important**: 
- `PYTHON_API` is for server-side calls
- `NEXT_PUBLIC_PYTHON_API` is for client-side calls
- Both should point to the same backend URL

---

## 🚀 Next Steps After Deployment

1. Monitor Vercel analytics
2. Set up error tracking (Sentry)
3. Configure custom domain
4. Set up GitHub Actions for CI/CD
5. Add automated tests
6. Monitor backend performance

---

## 📞 Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **GitHub Help**: https://docs.github.com
- **Railway Docs**: https://docs.railway.app

---

## ✅ Quick Command Reference

```powershell
# Git operations
git init                          # Initialize repo
git add .                         # Stage all changes
git commit -m "message"           # Commit changes
git push origin main              # Push to GitHub
git pull origin main              # Pull from GitHub
git log --oneline                 # View commit history

# GitHub
git remote add origin [URL]       # Add remote repository
git remote set-url origin [URL]   # Change remote URL
git remote -v                     # View remote repositories

# Vercel (if CLI installed)
vercel                            # Deploy/check status
vercel env pull                   # Pull env variables
vercel logs                       # View deployment logs
```

---

Ready to deploy! Follow the steps above and your company extractor will be live! 🎉
