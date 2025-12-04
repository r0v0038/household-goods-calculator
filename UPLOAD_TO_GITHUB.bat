@echo off
REM Batch script to upload project to GitHub
REM Created by Batman (Code Puppy)

echo ========================================
echo Uploading to GitHub...
echo ========================================
echo.

REM Navigate to project directory
cd /d "C:\Users\r0v0038\OneDrive - Walmart Inc\1. Code Puppy\Household Good"

echo Step 1: Initializing Git repository...
git init

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating commit...
git commit -m "Initial commit: Household Goods Calculator with discount feature"

echo.
echo Step 4: Setting main branch...
git branch -M main

echo.
echo Step 5: Adding remote repository...
git remote add origin https://github.com/r0v0038/household-goods-calculator.git

echo.
echo Step 6: Pushing to GitHub...
echo When prompted, enter your GitHub credentials:
echo Username: r0v0038
echo Password: Rvaj031992
echo.
git push -u origin main

echo.
echo ========================================
echo Upload complete!
echo ========================================
echo.
echo Check your GitHub repo:
echo https://github.com/r0v0038/household-goods-calculator
echo.
pause