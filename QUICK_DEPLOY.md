# ⚡ Quick Deploy - Get Online in 5 Minutes!

## 🎯 Option 1: Render.com (EASIEST - FREE)

### Step-by-Step:

1. **Push your code to GitHub:**
   ```bash
   # If you haven't already
   git init
   git add .
   git commit -m "Household goods calculator ready for deployment"
   
   # Create a new repo on GitHub.com, then:
   git remote add origin https://github.com/YOUR-USERNAME/household-goods-calculator.git
   git push -u origin main
   ```

2. **Go to Render.com:**
   - Visit: https://render.com
   - Click "Get Started for Free"
   - Sign up with your GitHub account

3. **Create Web Service:**
   - Click "New +" in the top right
   - Select "Web Service"
   - Click "Connect" next to your GitHub repository
   - Render will auto-detect it's a Python app!

4. **Configure (most fields auto-filled):**
   - **Name:** `household-goods-calculator` (or whatever you want)
   - **Environment:** Python 3 (auto-detected)
   - **Build Command:** `pip install -r requirements.txt` (auto-filled)
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4` (auto-filled)
   - **Instance Type:** Free

5. **Click "Create Web Service"**

6. **Wait 3-5 minutes** ☕ (watch the logs!)

7. **Get Your Live URL!** 🎉
   - You'll see it at the top: `https://household-goods-calculator.onrender.com`
   - Click it to open your calculator!

### 🔗 Share Your Link:

**Single Calculator:**  
`https://household-goods-calculator.onrender.com/`

**Bulk Upload:**  
`https://household-goods-calculator.onrender.com/bulk`

### ⚠️ Note about Free Tier:
- App "sleeps" after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Upgrade to $7/month for 24/7 uptime (if needed)

---

## 🚀 Option 2: Railway.app (FASTEST)

### Step-by-Step:

1. **Push to GitHub** (same as above if not done)

2. **Go to Railway:**
   - Visit: https://railway.app
   - Click "Login with GitHub"

3. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-deploys! 🎉

4. **Get Your URL:**
   - Click "Settings"
   - Under "Domains", click "Generate Domain"
   - You'll get: `https://household-goods-calculator.up.railway.app`

### 💰 Railway Pricing:
- Free: $5 credit/month (~500 hours)
- No sleep - always available!
- Upgrade: $5/month for more resources

---

## 🐳 Option 3: Docker + Your Own Server

### If you have a server/VM:

```bash
# Build the image
docker build -t household-goods-calculator .

# Run it
docker run -d -p 80:5000 --name household-calc household-goods-calculator

# Access at: http://your-server-ip/
```

Or use docker-compose:

```bash
docker-compose up -d
```

---

## 🏢 Option 4: Walmart Azure (Internal)

### For internal Walmart deployment:

1. **Contact your DevOps team** or Slack #cloud-support

2. **Provide them:**
   - This GitHub repository
   - Requested subdomain: `household-goods-calculator.walmart.com`
   - Resource requirements: 1 CPU, 2GB RAM

3. **They'll deploy and give you:**
   - Internal URL: `https://household-goods-calculator.walmart.com`
   - SSL certificate (automatic)
   - Monitoring dashboard

---

## ✅ After Deployment - Test Checklist

### Test Single Calculator:
1. Go to your URL: `https://your-app.com/`
2. Fill in:
   - Origin: Bentonville, AR
   - Destination: Seattle, WA
   - Weight: 5000
3. Click "Calculate Should Cost"
4. Should see results! ✓

### Test Bulk Upload:
1. Go to: `https://your-app.com/bulk`
2. Click "Download Excel Template"
3. Upload the same template back
4. Click "Process Calculations"
5. Should see 3 successful results! ✓

### Test Health:
1. Go to: `https://your-app.com/health`
2. Should show: `{"status": "healthy"}` ✓

---

## 💬 Share With Your Team

### Send this message:

> 🎉 **Household Goods Calculator is Live!**
> 
> **Single Move Calculator:**  
> https://your-app-url.com/
> 
> **Bulk Upload (Excel):**  
> https://your-app-url.com/bulk
> 
> Features:
> ✅ Calculate should cost for household goods moves
> ✅ Distance-based and weight-based pricing
> ✅ Regional adjustments
> ✅ Bulk upload via Excel file
> ✅ Download detailed cost breakdowns
> 
> Try it out and let me know what you think!

---

## 🔧 Updating Your App

When you make changes:

### Render/Railway (Auto-deploy):
```bash
git add .
git commit -m "Updated feature X"
git push
# Automatically deploys! 🎉
```

### Docker:
```bash
docker build -t household-goods-calculator .
docker stop household-calc
docker rm household-calc
docker run -d -p 80:5000 --name household-calc household-goods-calculator
```

---

## 🎯 My Recommendation

**For quick sharing:** Use **Render.com** (free, easy, 5 minutes)

**For Walmart internal:** Use **Azure App Service** (enterprise, supported)

**For best free tier:** Use **Railway.app** (no sleep, fast, $5 free credit)

**For full control:** Use **Docker** on your own server

---

## 🚀 Ready to Deploy?

Pick an option above and follow the steps! You'll be live in minutes! 🐶

**Questions?** Check the full [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed troubleshooting.

---

**Built with 🐶 by Batman (code-puppy)**
