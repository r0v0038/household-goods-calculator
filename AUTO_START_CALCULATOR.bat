@echo off
REM Auto-start Household Goods Calculator
REM This script starts the calculator in a new window

title Household Goods Calculator - Auto Start

cd /d "%~dp0"

echo ========================================
echo  Household Goods Calculator
echo  Starting automatically...
echo ========================================
echo.

REM Start in a new window so it doesn't block
start "Household Goods Calculator" cmd /k START_WITH_PROXY.bat

echo.
echo Calculator server starting in new window!
echo Access at: http://localhost:8080
echo.
echo This window will close in 3 seconds...
timeout /t 3 /nobreak >nul
