@echo off
REM Setup script to add Household Goods Calculator to Windows Startup (Silent)

REM Get the current directory
set SCRIPT_DIR=%~dp0

REM Get the Startup folder path
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

REM Create a VBS script to create the shortcut
set VBS_SCRIPT=%TEMP%\create_shortcut.vbs

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = "%STARTUP_FOLDER%\Household Goods Calculator.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%SCRIPT_DIR%AUTO_START_CALCULATOR.bat" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_SCRIPT%"
echo oLink.Description = "Household Goods Calculator - Auto Start" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

REM Run the VBS script
cscript //nologo "%VBS_SCRIPT%"

REM Clean up
del "%VBS_SCRIPT%"

echo Auto-start configured successfully!
