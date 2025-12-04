# 🔧 Walmart Proxy Fix - Can't Connect to Localhost

## ⚡ FASTEST FIX (Try This First!)

### Use Your Network IP Instead of Localhost:

1. **Double-click:** `START_PRODUCTION_WITH_PROXY_BYPASS.bat`

2. **Wait for the server to start** (you'll see the startup message)

3. **Open your browser and go to:**
   ```
   http://10.97.112.102:8080
   ```
   (NOT localhost - use the IP address!)

**Why this works:** Using your actual IP address bypasses the localhost proxy issue entirely!

---

## 🛠️ If That Doesn't Work: Fix Your Browser Proxy Settings

### Method 1: Automatic Fix Script

**Double-click:** `FIX_BROWSER_PROXY.bat`

This will open Windows proxy settings for you. Follow the on-screen instructions.

### Method 2: Manual Fix (Edge/Chrome)

1. **Open Edge or Chrome**

2. **Go to Settings:**
   - Edge: `edge://settings/system`
   - Chrome: `chrome://settings/system`

3. **Click** "Open your computer's proxy settings"

4. **Click** "LAN settings" button

5. **Click** "Advanced" button

6. **In the "Exceptions" box, add:**
   ```
   localhost;127.0.0.1;10.97.112.102
   ```

7. **Click OK** on all dialogs

8. **Restart your browser**

9. **Try again:** `http://127.0.0.1:8080`

### Method 3: Windows Settings (Alternative)

1. **Press** `Windows + I` to open Settings

2. **Go to:** Network & Internet → Proxy

3. **Under "Manual proxy setup"**, click **Edit**

4. **Add to "Don't use proxy server for addresses beginning with":**
   ```
   localhost;127.0.0.1;10.97.112.102
   ```

5. **Click** Save

6. **Restart your browser**

---

## 🎯 Testing Your Fix

### After fixing proxy settings, test these URLs:

✅ **Try each one until one works:**

1. `http://10.97.112.102:8080` ← **TRY THIS FIRST!**
2. `http://127.0.0.1:8080`
3. `http://localhost:8080`

### You should see:
- The Household Goods Calculator page
- Forms for Origin, Destination, Weight
- "Calculate Should Cost" button

---

## 🔍 Troubleshooting

### "Site can't be reached" or "Connection refused"

**Check 1: Is the server running?**
```cmd
netstat -ano | findstr :8080
```
You should see: `TCP    0.0.0.0:8080    0.0.0.0:0    LISTENING`

If not, start the server:
```cmd
cd C:\Users\r0v0038\household-goods-calculator
python production_server.py
```

**Check 2: Try ALL the URLs above**
- Sometimes one works when others don't
- Network IP (10.97.112.102) usually bypasses proxy issues

**Check 3: Try a different browser**
- Edge
- Chrome  
- Firefox
- Internet Explorer (if desperate!)

### "This site can't provide a secure connection"

**Problem:** You're trying to use HTTPS

**Solution:** Make sure URL starts with `http://` NOT `https://`
```
✅ http://10.97.112.102:8080
❌ https://10.97.112.102:8080
```

### Port 8080 Already in Use

**Edit:** `production_server.py`

**Change line:**
```python
port = int(os.environ.get('PORT', 8080))  # Change 8080 to 8081
```

**Then try:** `http://10.97.112.102:8081`

---

## 🏢 Still Not Working? IT Support Options

### Request from Walmart IT:

**Ticket Subject:** "Localhost Proxy Bypass for Development"

**Request:**
> Please add the following to my proxy bypass list:
> - localhost
> - 127.0.0.1
> - 10.97.112.102 (my workstation IP)
>
> This is needed for local web application development and testing.

**Alternative:** Ask if they can temporarily disable proxy for your machine

---

## 🌐 Deploy to Cloud (Skip Localhost Issues!)

If you can't get localhost working, **deploy to the cloud instead:**

**Railway.app (Recommended):**
- See: `DEPLOY_TO_RAILWAY.md`
- Get a public URL: `https://your-app.up.railway.app`
- No proxy issues!
- Always accessible
- Free $5/month credit

**Azure App Service (Walmart Internal):**
- See: `DEPLOYMENT_GUIDE.md`
- Get internal Walmart URL
- Managed by IT
- Production-ready

---

## 📋 Quick Reference Card

**START SERVER:**
```
Double-click: START_PRODUCTION_WITH_PROXY_BYPASS.bat
```

**ACCESS URLs (Try in order):**
```
1. http://10.97.112.102:8080  ← Best option!
2. http://127.0.0.1:8080
3. http://localhost:8080
```

**FIX BROWSER:**
```
Double-click: FIX_BROWSER_PROXY.bat
Add to exceptions: localhost;127.0.0.1;10.97.112.102
```

**CHECK IF RUNNING:**
```cmd
netstat -ano | findstr :8080
```

---

## ✅ Success Checklist

- [ ] Server is running (green checkmark in terminal)
- [ ] Tried IP address: `http://10.97.112.102:8080`
- [ ] Added proxy exceptions in browser
- [ ] Restarted browser after changing settings
- [ ] Can see the calculator page
- [ ] Can perform a calculation successfully

---

**Still stuck? Consider deploying to Railway (5 minutes, no localhost needed!)** 🚀

See: `DEPLOY_TO_RAILWAY.md`

---

**Created by Batman (code-puppy) 🐶 - Walmart Edition**
