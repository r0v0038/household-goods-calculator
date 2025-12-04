@echo off
REM Create desktop shortcut for Household Goods Calculator

title Create Desktop Shortcut

echo ========================================
echo  Creating Desktop Shortcut
echo ========================================
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0

REM Get the Desktop folder path
set DESKTOP=%USERPROFILE%\Desktop

echo Creating shortcut on desktop...
echo.

REM Create a VBS script to create the shortcut
set VBS_SCRIPT=%TEMP%\create_desktop_shortcut.vbs

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = "%DESKTOP%\Household Goods Calculator.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%SCRIPT_DIR%START_WITH_PROXY.bat" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_SCRIPT%"
echo oLink.Description = "Household Goods Calculator" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

REM Run the VBS script
cscript //nologo "%VBS_SCRIPT%"

REM Clean up
del "%VBS_SCRIPT%"

echo.
echo ========================================
echo  SUCCESS!
echo ========================================
echo.
echo Desktop shortcut created!
echo You can now launch the calculator from
echo your desktop.
echo.
echo ========================================
echo.
timeout /t 3 /nobreak >nul
