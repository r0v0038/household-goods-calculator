# 🚀 Deployment Guide - Household Goods Calculator

## Overview

This guide provides multiple deployment options to make your calculator accessible to anyone with a link.

---

## ⚡ Quick Deploy Options (Recommended)

### Option 1: Render.com (FREE & EASIEST) ⭐

**Best for:** Quick deployment, free hosting, automatic SSL

#### Steps:

1. **Create a free account** at [render.com](https://render.com)

2. **Click "New +"** → **"Web Service"**

3. **Connect your Git repository** (or upload code)
   - If you don't have a Git repo, create one:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin <your-github-url>
     git push -u origin main
     ```

4. **Configure the service:**
   - **Name:** household-goods-calculator
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120`

5. **Click "Create Web Service"**

6. **Get your live URL:** `https://household-goods-calculator.onrender.com`

**⏱ Deployment time:** ~5 minutes  
**💰 Cost:** FREE (with auto-sleep after 15 min inactivity)  
**🔒 SSL:** Automatic HTTPS  

---

### Option 2: Railway.app (FREE & FAST) ⭐

**Best for:** Fast deployment, great developer experience

#### Steps:

1. **Sign up** at [railway.app](https://railway.app) (use GitHub login)

2. **Click "New Project"** → **"Deploy from GitHub repo"**

3. **Select your repository**

4. **Railway auto-detects** Python and deploys!

5. **Get your URL:** Click "Generate Domain" in settings

**⏱ Deployment time:** ~3 minutes  
**💰 Cost:** FREE ($5 credit/month, ~500 hours)  
**🔒 SSL:** Automatic HTTPS  

---

### Option 3: Azure App Service (Walmart Standard) 🏢

**Best for:** Walmart internal deployment, enterprise support

#### Prerequisites:
- Azure account (ask your Walmart IT/DevOps team)
- Azure CLI installed

#### Steps:

1. **Login to Azure:**
   ```bash
   az login
   ```

2. **Create a resource group:**
   ```bash
   az group create --name household-goods-rg --location eastus
   ```

3. **Create an App Service plan:**
   ```bash
   az appservice plan create --name household-goods-plan --resource-group household-goods-rg --sku B1 --is-linux
   ```

4. **Create the web app:**
   ```bash
   az webapp create --resource-group household-goods-rg --plan household-goods-plan --name household-goods-calc --runtime "PYTHON:3.11"
   ```

5. **Deploy your code:**
   ```bash
   # Option A: From local Git
   git remote add azure <azure-git-url>
   git push azure main
   
   # Option B: From GitHub
   az webapp deployment source config --name household-goods-calc --resource-group household-goods-rg --repo-url <github-url> --branch main
   ```

6. **Configure startup command:**
   ```bash
   az webapp config set --resource-group household-goods-rg --name household-goods-calc --startup-file "gunicorn app:app --bind 0.0.0.0:$PORT --workers 4"
   ```

7. **Access your app:**
   - URL: `https://household-goods-calc.azurewebsites.net`

**⏱ Deployment time:** ~15 minutes  
**💰 Cost:** ~$13/month (B1 tier)  
**🔒 SSL:** Automatic HTTPS  
**✅ Walmart Approved:** Yes  

---

### Option 4: Heroku (Classic Choice)

**Best for:** Traditional PaaS, lots of add-ons

#### Steps:

1. **Install Heroku CLI:**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   heroku create household-goods-calculator
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Open your app:**
   ```bash
   heroku open
   ```

**⏱ Deployment time:** ~5 minutes  
**💰 Cost:** $7/month (Eco dyno) or $25/month (Basic)  
**🔒 SSL:** Automatic HTTPS  

---

## 🏢 Walmart Internal Deployment Options

### Option 5: Walmart Cloud Platform

**Contact your DevOps team for:**
- Internal Kubernetes cluster deployment
- Walmart's CI/CD pipeline integration
- Internal DNS and SSL certificates
- Load balancer configuration

#### Typical Walmart Deployment:

1. **Create a Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
   ```

2. **Build and push to Walmart's container registry**

3. **Deploy via Walmart's internal tools**

---

## 🔧 Environment Configuration

### Environment Variables (Optional)

You can set these in your deployment platform:

```bash
FLASK_ENV=production          # Disables debug mode
PORT=5000                      # Port (usually auto-set by platform)
MAX_CONTENT_LENGTH=16777216    # 16MB file upload limit
```

---

## 📊 Post-Deployment Checklist

### ✅ Test Your Deployment

1. **Single Calculator:**
   - Visit: `https://your-app-url.com/`
   - Test a calculation with valid data
   - Check that dropdowns work
   - Verify results display correctly

2. **Bulk Upload:**
   - Visit: `https://your-app-url.com/bulk`
   - Download the template
   - Upload the template
   - Process calculations
   - Download results Excel file

3. **Health Check:**
   - Visit: `https://your-app-url.com/health`
   - Should return: `{"status": "healthy"}`

### ✅ Share the Link

Once deployed, share these URLs:

- **Main Calculator:** `https://your-app-url.com/`
- **Bulk Upload:** `https://your-app-url.com/bulk`

---

## 🚨 Troubleshooting

### Problem: App crashes on startup

**Solution:** Check logs for missing dependencies
```bash
# Render/Railway: Check dashboard logs
# Azure: az webapp log tail --name household-goods-calc --resource-group household-goods-rg
# Heroku: heroku logs --tail
```

### Problem: File upload fails

**Solution:** Increase memory/timeout limits in platform settings

### Problem: Slow distance calculation

**Solution:** 
- Use manual distances in Excel uploads
- Consider caching geocoding results
- Upgrade to a paid tier for better performance

### Problem: App sleeps after inactivity (free tiers)

**Solutions:**
- Upgrade to paid tier for 24/7 uptime
- Use a ping service (UptimeRobot) to keep it awake
- Accept 30-second cold start on first request

---

## 🔒 Security Recommendations

### For Production Use:

1. **Add authentication** if needed:
   ```python
   # Simple password protection
   from flask_httpauth import HTTPBasicAuth
   auth = HTTPBasicAuth()
   
   @auth.verify_password
   def verify_password(username, password):
       if username == "walmart" and password == os.environ.get('APP_PASSWORD'):
           return username
   
   @app.route('/bulk')
   @auth.login_required
   def bulk_upload():
       return render_template('bulk.html')
   ```

2. **Rate limiting** for API endpoints:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/bulk/process', methods=['POST'])
   @limiter.limit("10 per minute")
   def process_bulk_file():
       # ...
   ```

3. **CORS configuration** if needed:
   ```python
   from flask_cors import CORS
   CORS(app, origins=["https://walmart.com"])
   ```

---

## 💡 Performance Tips

1. **Enable Caching:**
   - Cache geocoding results
   - Use Redis for session storage

2. **Optimize Workers:**
   - Adjust `--workers` based on dyno size
   - Use `--threads` for I/O-bound operations

3. **Monitor Performance:**
   - Set up application monitoring (New Relic, DataDog)
   - Track slow endpoints
   - Monitor memory usage

---

## 📞 Support

### Need Help?

1. **Check logs** first (see troubleshooting above)
2. **Review error messages** carefully
3. **Test locally** before deploying
4. **Contact your DevOps team** for Walmart-specific deployments

---

## 🎯 Recommended Deployment for Different Scenarios

| Scenario | Recommended Platform | Why |
|----------|---------------------|-----|
| Quick prototype/demo | **Render.com** | Free, fast, automatic SSL |
| Internal Walmart use | **Azure App Service** | Enterprise support, compliance |
| External sharing | **Railway.app** | Fast, reliable, great UX |
| Long-term production | **Azure App Service** | Scalable, supported, compliant |
| Budget-conscious | **Render.com** (free tier) | No cost, decent performance |

---

## 🎉 Quick Start (Fastest Deploy)

**Deploy in 3 minutes with Render:**

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect this repository
5. Render auto-detects settings
6. Click "Create Web Service"
7. Wait 3 minutes
8. Get your link: `https://household-goods-calculator.onrender.com`
9. Share with anyone! 🎉

---

**Built with 🐶 by Batman (code-puppy)**
