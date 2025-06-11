@echo off
title Create Desktop Shortcut
color 0B

echo.
echo 🔗 Creating Desktop Shortcut for Multi Coordinates Clicker
echo ================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "SHORTCUT_NAME=Multi Coordinates Clicker.lnk"
set "DESKTOP=%USERPROFILE%\Desktop"

REM Check if Desktop folder exists and is writable
echo Checking desktop permissions...
if not exist "%DESKTOP%" (
    echo ❌ Desktop folder not found at: %DESKTOP%
    echo Trying alternative desktop location...
    set "DESKTOP=%PUBLIC%\Desktop"
)

REM Test write permissions by creating a temp file
echo test > "%DESKTOP%\temp_test.txt" 2>nul
if exist "%DESKTOP%\temp_test.txt" (
    del "%DESKTOP%\temp_test.txt" 2>nul
    echo ✅ Desktop write permissions OK
) else (
    echo ⚠️ No write permissions to desktop, trying alternative methods...
    goto :alternative_method
)

REM Create VBS script to create shortcut
echo Creating shortcut using VBS method...
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%DESKTOP%\%SHORTCUT_NAME%"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%SCRIPT_DIR%run_app.bat"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%"
echo oLink.Description = "Multi Coordinates Clicker - Enhanced with Auto-Refresh"
echo oLink.IconLocation = "shell32.dll,25"
echo oLink.WindowStyle = 1
echo oLink.Save
) > temp_shortcut.vbs

cscript //nologo temp_shortcut.vbs 2>nul
set "VBS_RESULT=%ERRORLEVEL%"
del temp_shortcut.vbs 2>nul

if exist "%DESKTOP%\%SHORTCUT_NAME%" (
    echo ✅ Shortcut created successfully on Desktop!
    echo 📱 You can now double-click "%SHORTCUT_NAME%" to run the app
    echo 📌 To pin to taskbar: Right-click the shortcut → "Pin to taskbar"
    goto :success
) else (
    echo ❌ VBS method failed, trying alternative method...
    goto :alternative_method
)

:alternative_method
echo.
echo 🔄 Using PowerShell method (alternative)...

REM Create PowerShell script for shortcut creation
(
echo $WshShell = New-Object -comObject WScript.Shell
echo $Shortcut = $WshShell.CreateShortcut^("%DESKTOP%\%SHORTCUT_NAME%"^)
echo $Shortcut.TargetPath = "%SCRIPT_DIR%run_app.bat"
echo $Shortcut.WorkingDirectory = "%SCRIPT_DIR%"
echo $Shortcut.Description = "Multi Coordinates Clicker - Enhanced"
echo $Shortcut.IconLocation = "shell32.dll,25"
echo $Shortcut.Save^(^)
) > temp_shortcut.ps1

powershell -ExecutionPolicy Bypass -File temp_shortcut.ps1 2>nul
del temp_shortcut.ps1 2>nul

if exist "%DESKTOP%\%SHORTCUT_NAME%" (
    echo ✅ Shortcut created successfully using PowerShell!
    echo 📱 You can now double-click "%SHORTCUT_NAME%" to run the app
    echo 📌 To pin to taskbar: Right-click the shortcut → "Pin to taskbar"
    goto :success
) else (
    echo ❌ PowerShell method also failed
    goto :manual_method
)

:manual_method
echo.
echo 🔧 Manual Method (if automatic creation fails):
echo ================================================================
echo 1. Right-click on your Desktop
echo 2. Select "New" → "Shortcut"
echo 3. Browse to: %SCRIPT_DIR%run_app.bat
echo 4. Click "Next"
echo 5. Name it: Multi Coordinates Clicker
echo 6. Click "Finish"
echo 7. Right-click the new shortcut → "Pin to taskbar"
echo.
echo 📂 Application folder: %SCRIPT_DIR%
echo 📄 Target file: run_app.bat
echo.
goto :end

:success
echo.
echo 🎉 Success! The shortcut is ready to use.
echo 💡 Tip: You can also copy this shortcut to other locations:
echo    - Start Menu: %APPDATA%\Microsoft\Windows\Start Menu\Programs\
echo    - Quick Launch: Right-click taskbar → "Toolbars" → "Quick Launch"
echo.

:end
echo ================================================================
echo Press any key to continue...
pause >nul 