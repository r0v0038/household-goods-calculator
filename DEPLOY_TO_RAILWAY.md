# 🚀 Deploy to Railway - Live in 5 Minutes!

## Why Railway?
- ✅ **Always On** - No sleep (unlike Render free tier)
- ✅ **$5 Free Credit/Month** - ~500 hours of runtime
- ✅ **Auto-Deploy** - Push to GitHub = automatic deployment
- ✅ **Fast** - Deploy in under 5 minutes
- ✅ **Shareable URL** - Get a permanent link to share

---

## 📋 Prerequisites

1. A GitHub account (sign up at github.com if you don't have one)
2. Git installed on your computer
3. This calculator project (you already have it!)

---

## 🎯 Step-by-Step Deployment

### Step 1: Push to GitHub (First Time Only)

```bash
# Navigate to the project directory
cd C:\Users\r0v0038\household-goods-calculator

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Household goods calculator with updated tariffs"

# Go to github.com and create a new repository called 'household-goods-calculator'
# Then run these commands (replace YOUR-USERNAME):

git remote add origin https://github.com/YOUR-USERNAME/household-goods-calculator.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway

1. **Go to Railway:**
   - Visit: https://railway.app
   - Click **"Login with GitHub"**
   - Authorize Railway to access your GitHub

2. **Create New Project:**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose **"household-goods-calculator"** from the list
   - Railway will automatically detect it's a Python app!

3. **Wait for Deployment:**
   - Watch the logs as Railway builds and deploys
   - Takes about 2-3 minutes
   - You'll see: ✅ "Build successful" and ✅ "Deployed"

4. **Generate Public URL:**
   - Click **"Settings"** tab
   - Scroll to **"Domains"** section  
   - Click **"Generate Domain"**
   - You'll get something like: `household-goods-calculator-production.up.railway.app`

5. **Done!** 🎉
   - Your calculator is now LIVE!
   - Click the URL to test it
   - Share it with anyone!

---

## 🔗 Your Live URLs

Once deployed, you'll have:

**Single Calculator:**
```
https://your-app-name.up.railway.app/
```

**Bulk Upload:**
```
https://your-app-name.up.railway.app/bulk
```

**Health Check:**
```
https://your-app-name.up.railway.app/health
```

---

## 🔄 Updating Your Live App

When you make changes:

```bash
# Make your changes to the code
# Then:

git add .
git commit -m "Updated feature X"
git push

# Railway automatically deploys! 🎉
# Wait 1-2 minutes and your changes are live!
```

---

## 💰 Pricing & Usage

**Free Tier:**
- $5 credit per month (resets monthly)
- ~500 hours of runtime (~20 days)
- No sleep - always available!
- 1GB RAM, shared CPU

**If you run out:**
- Upgrade to **Hobby Plan: $5/month**
- Gets you unlimited hours + more resources

**Check usage:**
- Go to Railway dashboard
- Click on your project
- See usage under "Metrics"

---

## 🧪 Test Your Deployment

### Test 1: Single Calculator
1. Go to your Railway URL
2. Enter:
   - Origin: `Dallas, TX`
   - Destination: `Los Angeles, CA`
   - Weight: `5000`
3. Click "Calculate Should Cost"
4. Should show:
   - Interstate fee: 3%
   - CA sales tax: 7.25%
   - Total: ~10.25% in fees

### Test 2: Bulk Upload
1. Go to: `your-url.up.railway.app/bulk`
2. Click "Download Excel Template"
3. Upload it back
4. Should process 3 moves successfully

### Test 3: Health Check
1. Go to: `your-url.up.railway.app/health`
2. Should show: `{"status": "healthy"}`

---

## 🐛 Troubleshooting

### Build Failed?
- Check Railway logs for errors
- Make sure `requirements.txt` is in root directory
- Make sure `Procfile` exists (it should!)

### App Not Starting?
- Check that `PORT` environment variable is used in `app.py` (it is!)
- Railway automatically sets `PORT` - app should bind to it

### Can't Access URL?
- Make sure you clicked "Generate Domain" in Settings
- Wait 30 seconds after generation
- Try hard refresh: CTRL+SHIFT+R

---

## 📊 Monitoring

**View Logs:**
1. Go to Railway dashboard
2. Click your project
3. Click "Deployments" tab
4. See real-time logs

**View Metrics:**
1. Click "Metrics" tab
2. See:
   - CPU usage
   - Memory usage  
   - Request count
   - Response times

---

## 🎉 Share With Your Team

Once deployed, send this message:

> 🎉 **Household Goods Calculator is Live!**
>
> I've deployed a calculator for household goods moving costs.
>
> **🔗 Try it out:** https://your-app.up.railway.app
>
> **Features:**
> ✅ Calculate moving costs based on distance & weight
> ✅ Interstate commerce fees (3% for cross-state moves)
> ✅ State sales tax (all 50 states + DC, updated Dec 2025)
> ✅ Bulk upload via Excel for processing multiple moves
> ✅ Download detailed cost breakdowns
>
> **Example Calculation:**
> - Dallas, TX → Los Angeles, CA
> - 5,000 lbs
> - Result: Base cost + 3% interstate fee + 7.25% CA tax
>
> Let me know what you think!

---

## 🔐 Making it Private (Optional)

If you want to restrict access:

1. **Add Authentication:**
   - Modify `app.py` to require login
   - Use Flask-Login or simple password protection

2. **Use Railway Private Networking:**
   - Remove public domain
   - Access only via VPN or internal network

3. **Deploy to Walmart Azure:**
   - For internal-only access
   - See `DEPLOYMENT_GUIDE.md` for Azure instructions

---

## ⚡ Quick Reference

**Railway Dashboard:** https://railway.app/dashboard

**Common Commands:**
```bash
# Update your live app
git add .
git commit -m "Your changes"
git push

# View logs
# (Use Railway dashboard)

# Rollback to previous version
# (Use Railway dashboard > Deployments > Previous deployment > "Redeploy")
```

---

## 🆘 Need Help?

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **GitHub Issues:** Create issue in your repo

---

**Ready to deploy? Follow the steps above and you'll be live in 5 minutes!** 🚀🐶

---

**Created by Batman (code-puppy) - December 2025**
