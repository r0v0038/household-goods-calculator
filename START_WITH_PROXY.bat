@echo off
echo ========================================
echo  Household Goods Calculator
echo  With Proxy Server
echo ========================================
echo.
echo Starting Flask app on port 5000...
echo.

cd /d "%~dp0"

REM Start Flask in background
start "Flask App" cmd /c "python app.py"

echo Waiting for Flask to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Proxy server on port 8080...
echo.
echo ========================================
echo  ACCESS THE CALCULATOR AT:
echo  http://localhost:8080
echo  http://127.0.0.1:8080
echo ========================================
echo.
echo Press Ctrl+C to stop both servers
echo.

python proxy_server.py

pause
