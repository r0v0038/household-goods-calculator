# 🎉 Auto-Start Setup Complete!

## ✅ What Was Configured

Your Household Goods Calculator is now set to **start automatically** when you log in to Windows!

### Auto-Start Location
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Household Goods Calculator.lnk
```

### How It Works

1. **On Login:** Windows automatically runs the shortcut in your Startup folder
2. **Calculator Starts:** The server starts in a new window with proxy configuration
3. **Access Immediately:** Navigate to http://localhost:8080 in your browser

---

## 🔗 Quick Access

**Calculator URL:** http://localhost:8080

---

## 🛠️ Manual Control

### To Start Manually

Double-click any of these files:
- `START_WITH_PROXY.bat` - Normal start with proxy
- `AUTO_START_CALCULATOR.bat` - Auto-start version

### To Stop the Server

1. Find the terminal window titled "Household Goods Calculator"
2. Press `Ctrl+C` to stop the server

### To Disable Auto-Start

**Option 1: Via Windows Explorer**
1. Press `Win+R`
2. Type: `shell:startup`
3. Delete "Household Goods Calculator.lnk"

**Option 2: Via File Path**
1. Navigate to: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`
2. Delete "Household Goods Calculator.lnk"

### To Re-Enable Auto-Start

Run: `SETUP_AUTO_START_SILENT.bat`

---

## 📋 Files Created

- ✅ `AUTO_START_CALCULATOR.bat` - Auto-start wrapper script
- ✅ `SETUP_AUTO_START.bat` - Interactive setup (with prompts)
- ✅ `SETUP_AUTO_START_SILENT.bat` - Silent setup (no prompts)
- ✅ `CREATE_DESKTOP_SHORTCUT.bat` - Creates desktop shortcut
- ✅ Startup folder shortcut - Auto-runs on login

---

## 🚀 Next Steps

### Test It Now

1. **Logout and Login** to test auto-start
2. After login, a terminal window should appear
3. Navigate to **http://localhost:8080**
4. Your calculator should be ready to use!

### Create Desktop Shortcut (Optional)

If you want a desktop icon for manual launching:

1. Navigate to: `C:\Users\r0v0038\household-goods-calculator`
2. Right-click `START_WITH_PROXY.bat`
3. Select "Send to" → "Desktop (create shortcut)"
4. Rename the shortcut to "Household Goods Calculator"

---

## 🐶 Pro Tips

- The server runs in the background - no need to keep the terminal visible
- You can minimize the terminal window after it starts
- Bookmark http://localhost:8080 in your browser for quick access
- The calculator now uses the new **CapRelo-style weight-distance matrix** for transportation costs!

---

## 🆘 Troubleshooting

### Server Not Starting?

1. Check if Python is installed: `python --version`
2. Check if dependencies are installed: `pip list`
3. Run manually: `START_WITH_PROXY.bat`

### Port 8080 Already in Use?

Another application might be using port 8080. Stop that application or:
1. Edit `START_WITH_PROXY.bat`
2. Change the port numbers
3. Access the calculator at the new port

### Auto-Start Not Working?

1. Check if shortcut exists: `Win+R` → `shell:startup`
2. Verify the shortcut points to the correct file
3. Re-run: `SETUP_AUTO_START_SILENT.bat`

---

**Setup completed by Batman 🐶 - Your friendly code puppy!**
