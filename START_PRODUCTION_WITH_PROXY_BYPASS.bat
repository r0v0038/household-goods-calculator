@echo off
echo ========================================
echo  Household Goods Calculator
echo  PRODUCTION SERVER (Proxy Bypass)
echo ========================================
echo.
echo Setting up proxy bypass for localhost...
echo.

:: Set environment variables to bypass proxy for localhost
set NO_PROXY=localhost,127.0.0.1,10.97.112.102
set HTTP_PROXY=
set HTTPS_PROXY=

echo Installing waitress (if needed)...
uv pip install waitress --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com

echo.
echo ========================================
echo Starting Production Server
echo ========================================
echo.
echo Server will start on port 8080
echo.
echo IMPORTANT: Open your browser and go to:
echo.
echo    http://127.0.0.1:8080
echo.
echo OR use your network IP:
echo.
echo    http://10.97.112.102:8080
echo.
echo If browser says "Can't connect", add this to your
echo browser proxy bypass list:
echo.
echo    127.0.0.1;localhost;10.97.112.102
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

:: Start the production server
python production_server.py

pause
