@echo off
echo ========================================
echo  Household Goods Calculator
echo  PRODUCTION SERVER
echo ========================================
echo.
echo Installing production dependencies...
echo.

uv pip install waitress --index-url https://pypi.ci.artifacts.walmart.com/artifactory/api/pypi/external-pypi/simple --allow-insecure-host pypi.ci.artifacts.walmart.com

echo.
echo Starting production server...
echo.
echo Server will be available at:
echo   - http://localhost:8080
echo   - Share with others on your network!
echo.
echo Press CTRL+C to stop
echo.

python production_server.py

pause
