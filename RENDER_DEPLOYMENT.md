# 🚀 Deploy Backend to Render

## ✅ Why Render?

- ✅ **Free tier** with persistent storage
- ✅ **Easy Python/Flask deployment**
- ✅ **PostgreSQL database included** (optional)
- ✅ **Custom domains**
- ✅ **GitHub auto-deploy on push**
- ✅ **No credit card needed** for free tier

---

## 📋 Step-by-Step Guide

### Step 1: Create Render Account

1. Go to: https://render.com
2. Click "Sign up"
3. Sign up with GitHub
4. Authorize Render to access your GitHub account

---

### Step 2: Create Web Service

1. **Dashboard**: https://dashboard.render.com
2. Click **"New +"** button
3. Select **"Web Service"**

---

### Step 3: Connect GitHub Repository

1. Select your repository:
   - `Sachin-M-29/Company-Extractor`
   - Click "Connect"

2. If you see permission dialog, authorize Render

---

### Step 4: Configure Service

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | company-extractor-api |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python api.py` |
| **Instance Type** | Free |

---

### Step 5: Set Environment Variables

1. Scroll down to **"Environment"**
2. Click **"Add Environment Variable"**
3. Add these:

```
FLASK_ENV=production
OLLAMA_HOST=http://localhost:11434
```

---

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Build the service
   - Deploy it
3. Wait 3-5 minutes for deployment to complete

---

## 🎯 Get Your Backend URL

1. After deployment, you'll see a URL like:
   ```
   https://company-extractor-api.onrender.com
   ```

2. Copy this URL

3. Test it:
   ```powershell
   curl https://company-extractor-api.onrender.com/api/health
   ```
   Should return:
   ```json
   {"status": "ok", "message": "Company Extractor API is running"}
   ```

---

## 🔗 Update Frontend (Vercel)

1. Go to your **Vercel project settings**
2. Environment Variables
3. Update `NEXT_PUBLIC_PYTHON_API`:
   ```
   https://company-extractor-api.onrender.com
   ```
4. Vercel auto-redeploys

---

## 📊 Render vs Railway Comparison

| Feature | Render | Railway |
|---------|--------|---------|
| **Free Tier** | Yes (basic) | Yes ($5 credit) |
| **Build Time** | 2-3 min | 2-3 min |
| **Auto-deploy** | Yes (on push) | Yes (on push) |
| **Database** | PostgreSQL included | Included |
| **Custom Domain** | Yes (free) | Yes (free) |
| **Cold Start** | Yes (free tier) | Minimal |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Render wins for**: Simplicity, no credit card needed
**Railway wins for**: Performance, no cold starts

---

## ⚠️ Important Notes for Render

### Free Tier Limitations:
- **Cold starts**: Service sleeps after 15 min of inactivity
  - First request takes 10-30 seconds to wake up
  - Subsequent requests are fast
  
### Solution Options:
1. **Keep it free**: Accept cold starts (fine for demo)
2. **Upgrade to paid**: $7/month for always-on
3. **Use cron job**: Ping API every 10 minutes to keep warm

### Recommended for Production:
- Create free Render account
- Test for 1 month
- Upgrade to paid ($7-10/month) if needed for users

---

## 🔄 Auto-Deploy on GitHub Push

Render automatically deploys when you push to GitHub!

```powershell
# Make changes
git add .
git commit -m "Update extraction logic"
git push origin main

# Render sees the push and auto-deploys
# Check deployment status: https://dashboard.render.com
```

---

## 📝 Complete Deployment Checklist

### ✅ Frontend (Vercel):
- [ ] Go to https://vercel.com/new
- [ ] Import `Sachin-M-29/Company-Extractor`
- [ ] Set root directory to `nextjs-ui/`
- [ ] Add env var: `NEXT_PUBLIC_PYTHON_API` = (leave blank for now)
- [ ] Click Deploy
- [ ] Copy frontend URL

### ✅ Backend (Render):
- [ ] Go to https://render.com
- [ ] Sign up with GitHub
- [ ] Create new Web Service
- [ ] Connect `Sachin-M-29/Company-Extractor`
- [ ] Set Build: `pip install -r requirements.txt`
- [ ] Set Start: `python api.py`
- [ ] Click Deploy
- [ ] Wait for deployment (3-5 min)
- [ ] Copy backend URL

### ✅ Link Frontend to Backend:
- [ ] Go back to Vercel project settings
- [ ] Update `NEXT_PUBLIC_PYTHON_API` = your Render URL
- [ ] Vercel auto-redeploys
- [ ] Test extraction end-to-end

---

## 🧪 Testing Your Deployment

### 1. Test Backend:
```powershell
# Replace with your Render URL
curl https://company-extractor-api.onrender.com/api/health

# Should return:
# {"status": "ok", "message": "Company Extractor API is running"}
```

### 2. Test Frontend:
- Open: https://your-vercel-app.vercel.app
- Try extracting a company
- Results should appear

### 3. Check Logs:
- Render: Dashboard → Service → Logs
- Vercel: Dashboard → Project → Deployments → Logs

---

## 🆘 Troubleshooting

### "Service not found" or 404 Error
- Backend might still be deploying
- Check Render dashboard → Logs
- Wait for "successfully deployed" message

### "Cannot connect to backend"
- Check `NEXT_PUBLIC_PYTHON_API` is set in Vercel
- Verify URL matches your Render service URL
- Test backend directly with curl

### Extraction very slow (30+ seconds)
- **Likely**: Free tier cold start
- **Solution**: Upgrade to paid tier ($7/month for always-on)
- Or accept the slowness for now

### "Failed to scrape website"
- Expected behavior (no GPU, CPU slower)
- Increase timeout in UI settings
- Try different scrape method

---

## 💰 Pricing

### Render Free Tier:
- ✅ One free web service
- ✅ 750 hours/month (always free)
- ⏸️ Cold starts after 15 min inactivity
- 🌐 Free .onrender.com domain

### Render Paid Tier:
- $7/month for always-on (no cold starts)
- Better for production use
- Auto-scales with traffic

**Recommendation**: Start free, upgrade if needed

---

## 🚀 Quick Deployment Commands

```bash
# After deploying to Render, test the API
curl https://company-extractor-api.onrender.com/api/health

# Check backend logs
# Go to: https://dashboard.render.com

# View frontend logs
# Go to: https://vercel.com/dashboard
```

---

## 📱 Final Architecture

```
User Browser
    ↓
[Vercel Frontend] (https://your-app.vercel.app)
    ↓
[Render Backend] (https://company-extractor-api.onrender.com)
    ↓
[SQLite Database] (in app folder)
```

---

## ✅ You're All Set!

Your application is now deployed:
- **Frontend**: Vercel
- **Backend**: Render
- **Code**: GitHub (auto-deploy on push)
- **Cost**: Free or ~$7/month

🎉 **Your app is live on the internet!**

---

## 📚 Helpful Resources

- **Render Docs**: https://render.com/docs
- **Render Dashboard**: https://dashboard.render.com
- **Flask Deployment**: https://flask.palletsprojects.com/deployment/
- **GitHub Auto-Deploy**: https://render.com/docs/github

---

## 💬 Next Steps

1. **Deploy Backend to Render** (15 min)
2. **Update Vercel env variables** (2 min)
3. **Test extraction** (5 min)
4. **Share your live link!** 🚀

Good luck! 🎉
