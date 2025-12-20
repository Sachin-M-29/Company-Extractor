# 🚀 Quick Deployment Guide - GitHub + Vercel + Railway

## ✅ Step 1: Code Already Pushed to GitHub

Your code is **live on GitHub**! ✨

```
Repository: https://github.com/Sachin-M-29/Company-Extractor
Branch: main
Last commit: Initial commit with GPU acceleration & Contact page
```

**View your repo**: https://github.com/Sachin-M-29/Company-Extractor

---

## 🎯 Step 2: Deploy Frontend to Vercel (5 minutes)

### Quick Steps:

1. **Open Vercel Dashboard**:
   - Go to: https://vercel.com/dashboard
   - Sign in with GitHub (authorize if needed)

2. **Import Project**:
   - Click "Add New Project" → "Import Git Repository"
   - Select: `Sachin-M-29/Company-Extractor`

3. **Configure**:
   - Framework: **Next.js** (auto-detected)
   - Root Directory: **`nextjs-ui/`** ← Change this!
   - Click "Edit" if needed to set root

4. **Environment Variables** (click to add):
   ```
   Key: NEXT_PUBLIC_PYTHON_API
   Value: http://127.0.0.1:5000  (for now, update after backend deployed)
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your frontend is LIVE! 🎉

**Your frontend URL**: `https://your-project.vercel.app`

---

## 🔧 Step 3: Deploy Backend to Render (5 minutes)

### Quick Steps:

1. **Open Render**:
   - Go to: https://render.com
   - Sign up with GitHub (authorize access)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect: `Sachin-M-29/Company-Extractor`

3. **Configure**:
   - **Name**: company-extractor-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api.py`
   - **Instance Type**: Free

4. **Environment Variables**:
   - Add: `FLASK_ENV=production`

5. **Deploy**:
   - Click "Create Web Service"
   - Render auto-builds and deploys
   - Takes 3-5 minutes

6. **Get Your URL**:
   - After deployment, copy the URL
   - Example: `https://company-extractor-api.onrender.com`

**Your backend URL**: `https://company-extractor-api.onrender.com`

**Note**: Free tier has cold starts (10-30 sec first request after 15 min idle). Upgrade to $7/month for always-on.

---

## 🔗 Step 4: Connect Frontend to Backend (2 minutes)

1. **Go to Vercel Project Settings**:
   - https://vercel.com/dashboard
   - Select your project
   - Settings → Environment Variables

2. **Update the Variable**:
   - Find: `NEXT_PUBLIC_PYTHON_API`
   - Change value to: Your Railway backend URL
   - Example: `https://company-extractor-prod.up.railway.app`

3. **Redeploy Frontend**:
   - Vercel will auto-redeploy
   - Or go to Deployments → Latest → Redeploy

---

## ✅ Test Your Deployment

### Test Backend API:
```powershell
curl https://your-railway-url/api/health
```
Should return:
```json
{"status": "ok", "message": "Company Extractor API is running"}
```

### Test Frontend:
- Open: https://your-vercel-app.vercel.app
- Try extracting a company
- Results should appear!

---

## 🛑 Common Issues & Fixes

### "Cannot connect to backend"
**Fix**: 
- Make sure Railway URL is set in Vercel env vars
- Backend must be fully deployed on Railway
- Check CORS in `api.py`

### "Failed to scrape website"
**Fix**:
- Expected on Railway (no GPU)
- Increase timeout in settings
- Try different scrape method

### Deployment stuck
**Fix**:
- Check Railway logs
- Check Vercel build logs
- Restart deployment

---

## 📊 What You Now Have

| Component | Status | URL |
|-----------|--------|-----|
| GitHub Repo | ✅ Live | https://github.com/Sachin-M-29/Company-Extractor |
| Frontend | Deploy Now | vercel.app (after deploy) |
| Backend | Deploy Now | railway.app (after deploy) |
| Database | Included | SQLite in code |

---

## 🎓 Architecture After Deployment

```
User Browser
     ↓
[Vercel Frontend] (Next.js)
     ↓
[Railway Backend] (Flask)
     ↓
[SQLite Database] + [Ollama] (local or CPU)
```

---

## 📝 Detailed Guides

For more information, see:
- **[VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)** - Complete deployment guide
- **[GPU_SETUP.md](GPU_SETUP.md)** - GPU configuration
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference

---

## 🚀 Summary: Deployment in 3 Steps

1. **Vercel**: Import GitHub repo, set root to `nextjs-ui/`, deploy
2. **Railway**: Import GitHub repo, Python auto-detected, deploy
3. **Connect**: Update Vercel env vars with Railway URL, redeploy

**Time needed**: ~15 minutes total

**Cost**: Free (or ~$5/month if heavy usage)

---

Ready to deploy? Start with Vercel! 🎉
