# Complete Railway Deployment Guide for Roger

## 🎯 Your Deployment Details
- **Email:** roger.vang@walmart.com
- **GitHub Username:** r0v0038
- **Project:** Household Goods Calculator
- **Start Command:** `gunicorn app:app`
- **Python Version:** 3.11.0

---

# PART 1: Create GitHub Account & Repository

## Step 1.1: Create GitHub Account

1. Go to: **https://github.com/signup**
2. Enter your email: `roger.vang@walmart.com`
3. Create password (save it somewhere safe!)
4. Username: `r0v0038`
5. Click "Create account"
6. **Verify your email** (check your inbox for verification link)

## Step 1.2: Create a New Repository

1. After email verification, you'll be on GitHub home
2. Click the **"+" icon** (top right) → Select **"New repository"**
3. **Repository name:** `household-goods-calculator`
4. **Description:** "Household Goods Moving Cost Calculator"
5. **Visibility:** Public (so Railway can access it)
6. ✅ Check "Add a README file"
7. Click **"Create repository"**

## Step 1.3: Upload Your Code to GitHub

You have two options:

### Option A: Using Git Commands (Recommended)

**If you have Git installed:**

1. Open PowerShell or Command Prompt
2. Navigate to your project:
   ```powershell
   cd "C:\Users\r0v0038\OneDrive - Walmart Inc\1. Code Puppy\Household Good"
   ```

3. Initialize Git and upload:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: Household Goods Calculator with discount feature"
   git branch -M main
   git remote add origin https://github.com/r0v0038/household-goods-calculator.git
   git push -u origin main
   ```
   
   When prompted for password, use your **GitHub Personal Access Token** (see Step 1.4)

### Option B: Using GitHub Web Interface

1. Go to your new repository: https://github.com/r0v0038/household-goods-calculator
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop your project files:
   - `app.py`
   - `requirements.txt`
   - `runtime.txt`
   - `Procfile`
   - `calculator/` folder
   - `static/` folder
   - `templates/` folder
   - `data/` folder
4. Scroll down and click **"Commit changes"**

## Step 1.4: Create GitHub Personal Access Token (For Git Commands)

*Only needed if using Option A above*

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Token name:** `railway-deployment`
4. **Expiration:** 90 days (or longer)
5. **Scopes:** Check `repo` (all)
6. Click **"Generate token"**
7. **Copy the token** (you won't see it again!)
8. Use this token as your password when Git asks

---

# PART 2: Deploy to Railway

## Step 2.1: Sign Up for Railway

1. Go to: **https://railway.app/dashboard**
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Railway to access your GitHub

## Step 2.2: Create New Project

1. In Railway Dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Click **"Configure GitHub App"**
4. Select **Only select repositories** → Find and select: `household-goods-calculator`
5. Click **"Install & Authorize"**

## Step 2.3: Deploy Repository

1. Back in Railway, you should now see your repo listed
2. Click on **`household-goods-calculator`**
3. Railway will start deploying automatically!
4. Wait for the build to complete (takes 2-3 minutes)

## Step 2.4: Configure Environment Variables

1. In Railway Dashboard, go to **Variables** tab
2. Add these variables:
   ```
   KEY: PORT
   VALUE: 5000
   ```
   
   ```
   KEY: FLASK_ENV
   VALUE: production
   ```

3. Click "Deploy" or it auto-deploys

## Step 2.5: Get Your Public URL

1. Go to **Deployment** tab
2. Look for **"Public URL"** or **"Domain"**
3. It will look like: `https://household-goods-calculator-production.up.railway.app`
4. **Copy this URL!**

---

# PART 3: Test Your Deployment

1. Open your public URL in a browser
2. You should see the Household Goods Calculator!
3. Try:
   - Single calculator
   - Bulk upload
   - Discount feature

---

# Troubleshooting

## Issue: "Application Error" or Blank Page

**Solution:**
1. Go to Railway Dashboard
2. Click your project
3. Go to **Logs** tab
4. Look for error messages
5. Common issues:
   - Missing `Procfile` → Add it with: `web: gunicorn app:app`
   - Missing port binding → Should be automatic

## Issue: "Repository Not Found"

**Solution:**
1. Make sure your repo is PUBLIC (not private)
2. Re-authorize Railway: https://railway.app/account/integrations

## Issue: "Build Failed"

**Solution:**
1. Check if all files are uploaded to GitHub
2. Verify `requirements.txt` exists
3. Verify `runtime.txt` exists and has valid Python version

## Issue: Can't Connect to Database/APIs

**Solution:**
- This shouldn't happen with your app (no database)
- If distance service fails, it's due to network access
- Walmart proxy might block external API calls to Google Maps

---

# Success! 🎉

Once deployed, you have:
- ✅ Live public URL
- ✅ Discount feature working
- ✅ Full calculator functionality
- ✅ Bulk upload support
- ✅ Access from anywhere (even inside Walmart!)

**Share your URL:** Send the public URL to anyone and they can use your calculator!

---

# Next Steps (Optional)

- Set up custom domain (Railway → Settings → Domains)
- Enable auto-deploy on GitHub push
- Add more features
- Monitor logs and performance

---

# Support

If you get stuck:
1. Check Railway Docs: https://docs.railway.app
2. Check GitHub Help: https://docs.github.com
3. Ask me (Batman)! 🐕