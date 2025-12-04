# PowerShell script to create desktop shortcut for Household Goods Calculator

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$WshShell = New-Object -ComObject WScript.Shell
$ShortcutPath = Join-Path $DesktopPath "Household Goods Calculator.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = Join-Path $PSScriptRoot "START_WITH_PROXY.bat"
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.Description = "Household Goods Calculator - CapRelo Style"
$Shortcut.IconLocation = "%SystemRoot%\System32\shell32.dll,165"  # Calculator icon
$Shortcut.Save()

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Desktop Shortcut Created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nShortcut location: $ShortcutPath" -ForegroundColor Cyan
Write-Host "`nYou can now double-click the shortcut on" -ForegroundColor White
Write-Host "your desktop to start the calculator!" -ForegroundColor White
Write-Host "`n========================================`n" -ForegroundColor Green
