import os
import sys
import winshell
from win32com.client import Dispatch
import subprocess

def create_pinnable_shortcut():
    """Create a Windows shortcut that can be pinned to taskbar"""
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths
    python_exe = sys.executable
    script_path = os.path.join(current_dir, "multi_coordinates_clicker_enhanced.py")
    desktop = winshell.desktop()
    start_menu = winshell.start_menu()
    
    # Create shortcut on desktop
    desktop_shortcut = os.path.join(desktop, "Multi Coordinates Clicker.lnk")
    
    # Create shortcut in start menu
    start_menu_shortcut = os.path.join(start_menu, "Multi Coordinates Clicker.lnk")
    
    def create_shortcut(shortcut_path):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Set target to python executable with script as argument
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = current_dir
        shortcut.Description = "Multi Coordinates Clicker - Automated clipboard pasting tool"
        
        # Try to set icon (will be created when app runs)
        icon_path = os.path.join(current_dir, "temp_app_icon.ico")
        if os.path.exists(icon_path):
            shortcut.IconLocation = icon_path
        
        shortcut.save()
        print(f"Created shortcut: {shortcut_path}")
    
    try:
        # Create shortcuts
        create_shortcut(desktop_shortcut)
        create_shortcut(start_menu_shortcut)
        
        print("\n✅ Shortcuts created successfully!")
        print(f"📌 Desktop shortcut: {desktop_shortcut}")
        print(f"📌 Start Menu shortcut: {start_menu_shortcut}")
        print("\n📋 Instructions for pinning to taskbar:")
        print("1. Right-click on the desktop shortcut")
        print("2. Select 'Pin to taskbar'")
        print("   OR")
        print("1. Find 'Multi Coordinates Clicker' in Start Menu")
        print("2. Right-click and select 'Pin to taskbar'")
        
        # Ask if user wants to run the app
        response = input("\n🚀 Would you like to run the application now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            subprocess.Popen([python_exe, script_path])
            
    except Exception as e:
        print(f"❌ Error creating shortcuts: {e}")
        print("Try running as administrator or install required packages:")
        print("pip install pywin32 winshell")

if __name__ == "__main__":
    create_pinnable_shortcut() 