@echo off
echo =============================================
echo   Multi Coordinates Clicker Setup
echo   Making application pinnable to taskbar
echo =============================================
echo.

echo 📦 Installing required packages...
pip install -r requirements.txt

echo.
echo 📌 Creating shortcuts for taskbar pinning...
python create_pinnable_shortcut.py

echo.
echo ✅ Setup complete!
echo.
echo 📋 To pin to taskbar:
echo 1. Look for the shortcut on your desktop
echo 2. Right-click and select "Pin to taskbar"
echo    OR
echo 1. Search for "Multi Coordinates Clicker" in Start Menu
echo 2. Right-click and select "Pin to taskbar"
echo.
pause 