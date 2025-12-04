@echo off
echo ========================================
echo  Browser Proxy Bypass Fix
echo  For Walmart Corporate Network
echo ========================================
echo.
echo This will help you configure your browser to access
echo localhost servers while on Walmart's network.
echo.
echo OPTION 1: Edge/Chrome (Recommended)
echo ========================================
echo.
echo 1. Open Edge or Chrome
echo 2. Go to: edge://settings/system (or chrome://settings/system)
echo 3. Click "Open your computer's proxy settings"
echo 4. Click "LAN settings"
echo 5. Click "Advanced"
echo 6. In the "Exceptions" box, add:
echo.
echo    localhost;127.0.0.1;10.97.112.102
echo.
echo 7. Click OK on all dialogs
echo 8. Restart your browser
echo.
echo ========================================
echo.
pause
echo.
echo Opening Windows Proxy Settings for you...
echo.
start ms-settings:network-proxy
echo.
echo Manual steps:
echo 1. Scroll to "Manual proxy setup"
echo 2. Click "Edit" under "Use a proxy server"
echo 3. Add to "Don't use proxy for":
echo.
echo    localhost;127.0.0.1;10.97.112.102
echo.
echo 4. Save
echo 5. Restart browser
echo.
echo ========================================
echo OPTION 2: Quick Test with IP Address
echo ========================================
echo.
echo After starting the server, try accessing:
echo.
echo    http://10.97.112.102:8080
echo.
echo This sometimes bypasses the proxy issue!
echo.
pause
