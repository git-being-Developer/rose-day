# 🚀 Deployment Guide - Rose Day App

## 🌟 Recommended: Deploy on Railway (Easiest)

Railway is the easiest option for FastAPI apps with zero configuration needed!

### Steps:

1. **Push your code to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Rose Day App"
   git remote add origin https://github.com/YOUR_USERNAME/rose-day.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Choose "Deploy from GitHub repo"
   - Select your `rose-day` repository
   - Railway will auto-detect it's a Python app!

3. **Add Environment Variables**:
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add:
     - `SUPABASE_URL` = your_supabase_url
     - `SUPABASE_KEY` = your_supabase_key

4. **Configure Port** (Railway auto-detects but to be sure):
   - Railway will read from `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - No extra config needed!

5. **Deploy**: Railway automatically deploys! 🎉

**Your app will be live at**: `https://your-app-name.up.railway.app`

---

## 🔷 Option 2: Deploy on Render

Render is another excellent free option!

### Steps:

1. **Create `render.yaml`** in your project root:
   ```yaml
   services:
     - type: web
       name: rose-day
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: SUPABASE_URL
           sync: false
         - key: SUPABASE_KEY
           sync: false
   ```

2. **Deploy**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render auto-detects Python
   - Add environment variables in dashboard
   - Click "Create Web Service"

**Your app will be live at**: `https://your-app-name.onrender.com`

---

## 🟣 Option 3: Deploy on Vercel (With Configuration)

Vercel is great but needs a bit more setup for FastAPI.

### Steps:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`** in your project root:
   ```json
   {
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ],
     "env": {
       "SUPABASE_URL": "@supabase-url",
       "SUPABASE_KEY": "@supabase-key"
     }
   }
   ```

3. **Update `main.py`** - Add this at the bottom:
   ```python
   # For Vercel
   app = app
   ```

4. **Deploy**:
   ```bash
   vercel --prod
   ```

5. **Add Environment Variables**:
   - Go to Vercel Dashboard
   - Select your project → Settings → Environment Variables
   - Add `SUPABASE_URL` and `SUPABASE_KEY`
   - Redeploy

**Your app will be live at**: `https://your-app.vercel.app`

---

## 🔴 Option 4: Deploy on Fly.io

Fly.io is powerful and has a generous free tier!

### Steps:

1. **Install Fly CLI**:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login and Initialize**:
   ```bash
   fly auth login
   fly launch
   ```

3. **When prompted**:
   - App name: `rose-day` (or your choice)
   - Region: Choose closest to you
   - Database: No (we're using Supabase)
   - Deploy now: No (we need to add secrets first)

4. **Set Environment Variables**:
   ```bash
   fly secrets set SUPABASE_URL="your_supabase_url"
   fly secrets set SUPABASE_KEY="your_supabase_key"
   ```

5. **Deploy**:
   ```bash
   fly deploy
   ```

**Your app will be live at**: `https://rose-day.fly.dev`

---

## 🟢 Option 5: Deploy on Heroku

Classic and reliable!

### Steps:

1. **Create `Procfile`** in your project root:
   ```
   web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
   ```

2. **Create `runtime.txt`** (optional):
   ```
   python-3.11.0
   ```

3. **Deploy**:
   ```bash
   heroku login
   heroku create rose-day-app
   
   # Add environment variables
   heroku config:set SUPABASE_URL="your_url"
   heroku config:set SUPABASE_KEY="your_key"
   
   # Deploy
   git push heroku main
   ```

**Your app will be live at**: `https://rose-day-app.herokuapp.com`

---

## 🔶 Option 6: Deploy on PythonAnywhere

Good for beginners!

### Steps:

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Upload your code via "Files" tab
4. Open a Bash console and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Go to "Web" tab → Add a new web app
6. Choose "Manual configuration" → Python 3.10
7. Set WSGI configuration to point to your app
8. Add environment variables in "Environment variables" section

---

## ⚙️ Pre-Deployment Checklist

Before deploying, make sure:

- ✅ `.env` file is in `.gitignore` (never commit secrets!)
- ✅ `requirements.txt` is up to date
- ✅ Supabase database table is created (run `setup.sql`)
- ✅ Test locally: `uvicorn main:app --reload`
- ✅ All environment variables are set in the platform

---

## 🎯 Recommended Order (Easiest to Hardest):

1. **Railway** ⭐ - Best for beginners, zero config
2. **Render** - Also very easy, great free tier
3. **Fly.io** - Powerful, good for scaling
4. **Heroku** - Classic, well-documented
5. **Vercel** - Needs more setup for Python
6. **PythonAnywhere** - Good learning platform

---

## 🔧 Troubleshooting

### Port Issues
Most platforms set `PORT` environment variable. Make sure your app uses it:
```python
import os
port = int(os.getenv("PORT", 8000))
```

### Database Connection
- Verify Supabase credentials are correct
- Check if table exists
- Ensure RLS policies allow public access

### Static Files
All HTML is embedded, so no static file configuration needed!

---

## 🌐 Custom Domain (Optional)

Most platforms allow custom domains:
- Railway: Settings → Domains
- Vercel: Settings → Domains
- Render: Settings → Custom Domains
- Heroku: Settings → Domains

---

## 📊 Monitoring

After deployment, monitor your app:
- Check logs in platform dashboard
- Set up error alerts
- Monitor response times
- Check Supabase usage

---

**Need help?** Check the platform-specific documentation or create an issue!

🌹 Happy Deploying! 💝
