# 🚀 Live Demo Deployment Guide

## ✅ Git Repository
**GitHub Repository**: https://github.com/moturi311/nexatask-pro

Your code has been successfully pushed to GitHub!

---

## 🌐 Deploy to Render (Recommended - Free)

### Step 1: Sign Up / Log In
1. Go to [Render.com](https://render.com/)
2. Sign up or log in with your GitHub account

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Select the repository: **moturi311/nexatask-pro**

### Step 3: Configure Service
Render will auto-detect your `render.yaml` file. Verify these settings:

- **Name**: `nexatask-pro`
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: `Free` (or upgrade as needed)

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. Your live demo will be available at: `https://nexatask-pro.onrender.com`

### Important Notes
- Free tier may spin down after inactivity (takes ~30 seconds to wake up)
- Database (`tasks.db`) will persist on Render's filesystem
- For production, consider upgrading to a paid tier and using PostgreSQL

---

## 🔧 Alternative: Deploy to Railway

### Step 1: Sign Up
1. Go to [Railway.app](https://railway.app/)
2. Sign in with GitHub

### Step 2: Deploy
1. Click **"New Project"** → **"Deploy from GitHub repo"**
2. Select **moturi311/nexatask-pro**
3. Railway auto-detects Python and deploys
4. Your app will be live at: `https://nexatask-pro.up.railway.app`

---

## 🐳 Alternative: Deploy to Fly.io

### Step 1: Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login
```bash
fly auth login
```

### Step 3: Create fly.toml
Create a `fly.toml` file:
```toml
app = "nexatask-pro"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Step 4: Deploy
```bash
fly launch
fly deploy
```

Your app will be live at: `https://nexatask-pro.fly.dev`

---

## 📱 Quick Demo Access

Once deployed, share your live demo:

- **Render**: `https://nexatask-pro.onrender.com`
- **Railway**: `https://nexatask-pro.up.railway.app`
- **Fly.io**: `https://nexatask-pro.fly.dev`

---

## 🔄 Update Your Live Demo

Whenever you make changes:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

All platforms will **automatically redeploy** when you push to GitHub!

---

## 🎯 Features Included in Live Demo

✅ Add, complete, and delete tasks  
✅ Real-time statistics  
✅ Persistent SQLite database  
✅ Beautiful responsive UI  
✅ XSS protection  

---

## 📊 Monitor Your Live Demo

### Render
- Dashboard: https://dashboard.render.com
- View logs, metrics, and manage your service

### Railway
- Dashboard: https://railway.app/dashboard
- Real-time logs and analytics

### Fly.io
```bash
fly logs
fly status
```

---

## 🛠️ Troubleshooting

**App not loading?**
- Check deployment logs on your platform
- Verify `requirements.txt` has all dependencies
- Ensure `gunicorn` is installed

**Database issues?**
- SQLite works on all platforms
- For production, consider PostgreSQL
- Database persists on Render's free tier

**Port issues?**
- Render/Railway/Fly handle ports automatically
- No need to modify `app.py`

---

## 🎉 Success!

Your Personal Task Manager is now live! Share the link with anyone to showcase your project.

**Repository**: https://github.com/moturi311/nexatask-pro  
**Live Demo**: (Your deployment URL)

---

Built with ❤️ by moturi311
