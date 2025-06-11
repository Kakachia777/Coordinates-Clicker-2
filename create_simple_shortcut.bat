@echo off
title Simple Shortcut Creator
color 0E

echo.
echo 🔗 Simple Shortcut Creator for Multi Coordinates Clicker
echo ================================================================
echo.

set "APP_DIR=%~dp0"
set "APP_NAME=Multi Coordinates Clicker"

echo 📂 Application location: %APP_DIR%
echo 🎯 Target: run_app.bat
echo.

echo 🔧 Creating shortcut using Windows Explorer method...
echo.
echo INSTRUCTIONS:
echo ================================================================
echo 1. Windows Explorer will open to this folder
echo 2. Right-click on "run_app.bat"
echo 3. Select "Send to" → "Desktop (create shortcut)"
echo 4. The shortcut will appear on your desktop
echo 5. Rename it to "%APP_NAME%" if desired
echo 6. Right-click the desktop shortcut → "Pin to taskbar"
echo.

echo Press any key to open Windows Explorer...
pause >nul

REM Open Windows Explorer to the application folder
explorer "%APP_DIR%"

echo ✅ Windows Explorer opened!
echo 👆 Follow the instructions above to create your shortcut.
echo.
echo 💡 Alternative: You can also drag "run_app.bat" to your desktop
echo    while holding the RIGHT mouse button, then select "Create shortcuts here"
echo.
echo Press any key to exit...
pause >nul 