# 🔧 Proxy Setup Guide

If you're having trouble accessing the calculator at `http://127.0.0.1:5000` due to Walmart's corporate proxy, use one of these solutions:

## 🚀 Solution 1: Use the Proxy Server (EASIEST)

**Double-click:** `START_WITH_PROXY.bat`

This will:
1. Start the Flask app on port 5000
2. Start a proxy server on port 8080
3. Forward all requests to the Flask app

**Access the calculator at:**
```
http://localhost:8080
http://127.0.0.1:8080
```

---

## 🔓 Solution 2: Bypass Proxy for Localhost

**Double-click:** `PROXY_BYPASS_SETUP.bat`

Then choose option 1 to temporarily bypass the proxy for this session.

**Access the calculator at:**
```
http://127.0.0.1:5000
```

---

## ⚙️ Solution 3: Manual Proxy Bypass Configuration

### Windows Internet Options:

1. Press `Windows + R`
2. Type `inetcpl.cpl` and press Enter
3. Go to **Connections** tab
4. Click **LAN settings**
5. Click **Advanced** (under Proxy server section)
6. In the "Exceptions" box, add:
   ```
   localhost;127.0.0.1;10.97.112.102
   ```
7. Click **OK** on all dialogs
8. Restart your browser

**Access the calculator at:**
```
http://127.0.0.1:5000
```

---

## 🌐 Solution 4: Use Network IP Instead

If none of the above work, try accessing via your machine's IP address:

```
http://10.97.112.102:5000
```

This bypasses localhost entirely and uses your network IP.

---

## 🐍 Manual Proxy Server Start

If you prefer to start servers manually:

### Terminal 1 - Start Flask:
```bash
cd household-goods-calculator
python app.py
```

### Terminal 2 - Start Proxy:
```bash
cd household-goods-calculator
python proxy_server.py
```

Then access: `http://localhost:8080`

---

## 🔍 Troubleshooting

### Port 8080 already in use?

Edit `proxy_server.py` and change:
```python
PROXY_PORT = 8080  # Change to 8081, 8082, etc.
```

### Still can't connect?

1. Check Windows Firewall:
   - Search "Windows Defender Firewall"
   - Click "Allow an app through firewall"
   - Make sure Python is allowed

2. Try different browsers:
   - Chrome
   - Edge
   - Firefox

3. Check if Flask is actually running:
   - Open Command Prompt
   - Run: `netstat -ano | findstr :5000`
   - You should see a line with LISTENING

### Corporate proxy blocking everything?

Contact your IT department and request:
- Localhost (127.0.0.1) to be added to proxy bypass list
- Or permission to run local development servers

---

## 📞 Need Help?

If none of these solutions work, you may need to:
1. Contact Walmart IT support
2. Request proxy bypass for development purposes
3. Use a different network (like phone hotspot for testing)

---

**Happy Calculating! 🐶**
