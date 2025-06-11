# 🚀 Multi Coordinates Clicker - Enhanced

A powerful desktop application that allows you to click at multiple screen coordinates and paste clipboard content at those locations with advanced features and automation.

## ✨ Features

- **Multiple Coordinates**: Set and manage multiple coordinate positions
- **Auto-Refresh Clipboard**: Automatically updates clipboard content every 2 seconds
- **Real-time Preview**: Live clipboard content preview with timestamps
- **Batch Processing**: Execute actions at multiple locations in sequence
- **Adjustable Settings**: Individual delays and Enter key options per coordinate
- **Quick Position Capture**: Get current mouse position with one click
- **Taskbar Pinnable**: Pin to Windows taskbar like any regular application
- **Custom Icon**: Professional app icon for easy identification
- **One-Click Launch**: Easy desktop shortcut creation
- **Modern UI**: Beautiful, dark-themed interface with better contrast
- **Activity Logs**: Detailed logging of all operations
- **Smart Controls**: Enable/disable auto-refresh as needed

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### Option 1: Easy Setup (Recommended for Taskbar Pinning)
1. Double-click `setup_pinnable_app.bat` to:
   - Install all dependencies automatically
   - Create shortcuts on desktop and start menu
   - Set up the app with proper icon for taskbar pinning
2. Right-click the desktop shortcut and select "Pin to taskbar"
3. The app will now appear as a regular application in your taskbar!

### Option 2: Manual Shortcut Creation
1. Double-click `create_shortcut.bat` to create a desktop shortcut
2. Double-click the "Multi Coordinates Clicker" shortcut on your desktop
3. The app will launch automatically!

### Option 3: Direct Launch
1. Double-click `run_app.bat` 
2. The application will start with all dependencies checked

### Option 4: Python Command
```bash
python multi_coordinates_clicker_enhanced.py
```

## 📌 Pinning to Taskbar

After running the setup, you can pin the application to your Windows taskbar:

**Method 1 - From Desktop:**
1. Right-click the "Multi Coordinates Clicker" shortcut on your desktop
2. Select "Pin to taskbar"

**Method 2 - From Start Menu:**
1. Click the Start button and search for "Multi Coordinates Clicker"
2. Right-click the result and select "Pin to taskbar"

The application will now behave like any regular Windows application with its own icon in the taskbar!

## 📋 How to Use

1. **Copy Text First**: Copy the text you want to paste to your clipboard

2. **Auto-Refresh**: The clipboard updates automatically every 2 seconds
   - Toggle auto-refresh on/off with the "⏰ Auto-Refresh" button
   - Use "🔄 Refresh Now" for manual updates

3. **Configure Coordinates**: 
   - Use the main tab's coordinate table to see all positions
   - Click "🎯 Get Pos" to capture your current mouse position
   - Edit coordinates directly in the Quick Settings panel

4. **Customize Settings**:
   - Set individual delays for each coordinate
   - Choose whether to press Enter after pasting
   - Name each position for easy identification

5. **Execute Sequence**: Click "🚀 START SEQUENCE" to:
   - Wait 3 seconds for you to switch applications
   - Visit each coordinate in order
   - Click and paste clipboard content
   - Apply individual delays and Enter key presses

## Safety Features

- **Failsafe**: Move your mouse to the top-left corner of the screen to abort any pyautogui operation
- **Input Validation**: The app validates all inputs before execution
- **Threading**: UI remains responsive during operations

## Requirements

- Windows 10/11 (tested)
- Python 3.6+
- pyautogui
- pyperclip
- Pillow (PIL)
- pywin32 (for Windows shortcuts)
- winshell (for Windows shortcuts)
- tkinter (usually included with Python)

## Notes

- Make sure the target application is ready to receive the pasted content
- The application works best with text-based content in the clipboard
- Some applications may require focus before pasting works properly
- The app creates a temporary icon file that's cleaned up when closing 