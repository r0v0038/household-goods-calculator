@echo off
echo ========================================
echo  Household Goods Calculator
echo  Starting server...
echo ========================================
echo.
echo Server will start on: http://localhost:5000
echo.
echo Opening browser in 3 seconds...
echo.

timeout /t 3 /nobreak > nul

:: Open browser
start http://localhost:5000

:: Start Flask server
echo Server starting... Press CTRL+C to stop.
echo.
python app.py
