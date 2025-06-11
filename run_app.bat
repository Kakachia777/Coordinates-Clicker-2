@echo off
title Multi Coordinates Clicker - Enhanced
color 0A

echo.
echo ================================================================
echo 🚀 Multi Coordinates Clicker - Enhanced
echo ================================================================
echo.
echo Starting application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.6+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import pyautogui, pyperclip" >nul 2>&1
if errorlevel 1 (
    echo ❌ Required packages not found. Installing...
    pip install pyautogui pyperclip
    if errorlevel 1 (
        echo ❌ Failed to install packages!
        pause
        exit /b 1
    )
)

echo ✅ All dependencies OK!
echo.

REM Run the application
echo 🚀 Launching Multi Coordinates Clicker - Enhanced...
echo ⏰ Auto-refresh: Clipboard will update every 10 seconds
echo 📋 Copy text before using the app!
echo.
python multi_coordinates_clicker_enhanced.py

if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error!
    pause
) else (
    echo.
    echo ✅ Application closed successfully!
    timeout /t 3 >nul
) 