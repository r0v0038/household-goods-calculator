@echo off
echo ========================================
echo  Proxy Bypass Configuration Helper
echo ========================================
echo.
echo This script will help you bypass the Walmart proxy
echo for localhost connections.
echo.
echo Choose an option:
echo.
echo [1] Set proxy bypass for current session only (TEMPORARY)
echo [2] Show current proxy settings
echo [3] Open Internet Options to manually configure
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto bypass_temp
if "%choice%"=="2" goto show_proxy
if "%choice%"=="3" goto open_settings
if "%choice%"=="4" goto end

goto end

:bypass_temp
echo.
echo Setting proxy bypass for localhost...
echo.
set HTTP_PROXY=
set HTTPS_PROXY=
set NO_PROXY=localhost,127.0.0.1,10.97.112.102

echo ✓ Proxy bypass configured for this session!
echo.
echo Environment variables set:
echo   NO_PROXY=%NO_PROXY%
echo   HTTP_PROXY=(cleared)
echo   HTTPS_PROXY=(cleared)
echo.
echo Note: This only affects programs launched from THIS command window.
echo.
echo Now starting the calculator...
echo.
timeout /t 3 /nobreak > nul
start "Calculator" cmd /k "cd /d %~dp0 && set NO_PROXY=localhost,127.0.0.1 && python app.py"
echo.
echo ✓ Calculator started with proxy bypass!
echo   Access at: http://127.0.0.1:5000
echo.
goto end

:show_proxy
echo.
echo Current Proxy Environment Variables:
echo.
echo HTTP_PROXY = %HTTP_PROXY%
echo HTTPS_PROXY = %HTTPS_PROXY%
echo NO_PROXY = %NO_PROXY%
echo.
echo Current Windows Proxy Settings:
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride
echo.
goto end

:open_settings
echo.
echo Opening Internet Options...
echo.
echo Manual Configuration Steps:
echo 1. Go to "Connections" tab
echo 2. Click "LAN settings"
echo 3. Click "Advanced" under Proxy server
echo 4. In "Exceptions" add: localhost;127.0.0.1;10.97.112.102
echo 5. Click OK on all dialogs
echo.
start inetcpl.cpl
goto end

:end
echo.
pause
