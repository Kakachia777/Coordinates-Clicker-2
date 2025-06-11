import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import pyperclip
import time
import threading
import json
import os
import base64
from PIL import Image, ImageDraw, ImageTk
import io

# Global color scheme - Modern dark theme with good contrast
COLORS = {
    'primary': '#2C3E50',      # Dark blue-gray for headers
    'secondary': '#34495E',    # Slightly lighter for secondary elements
    'success': '#27AE60',      # Green for success actions
    'danger': '#E74C3C',       # Red for danger actions
    'warning': '#F39C12',      # Orange for warnings
    'info': '#3498DB',         # Blue for info
    'light': '#ECF0F1',        # Light gray for backgrounds
    'dark': '#000000',         # Dark for text
    'accent': '#16A085',       # Teal for accents
    'bg': '#FFFFFF',           # White background
    'text': '#000000',         # Dark text for contrast
    'text_on_primary': '#FFFFFF' # White text for use on dark backgrounds like primary color
}

def create_app_icon():
    """Create a professional-looking app icon"""
    # Create a 32x32 icon with a modern design
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background circle
    draw.ellipse([2, 2, 30, 30], fill='#2C3E50', outline='#3498DB', width=2)
    
    # Draw cursor/target symbol
    # Crosshair
    draw.line([16, 8, 16, 12], fill='#FFFFFF', width=2)
    draw.line([16, 20, 16, 24], fill='#FFFFFF', width=2)
    draw.line([8, 16, 12, 16], fill='#FFFFFF', width=2)
    draw.line([20, 16, 24, 16], fill='#FFFFFF', width=2)
    
    # Center dot
    draw.ellipse([14, 14, 18, 18], fill='#E74C3C')
    
    return img

class MultiCoordinatesClicker:
    def __init__(self, root):
        self.root = root
        
        # Set window properties for taskbar pinning
        self.root.title("Multi Coordinates Clicker")
        self.root.geometry("1800x700")
        self.root.resizable(True, True)
        
        # Create and set the application icon
        try:
            icon_img = create_app_icon()
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(True, self.icon_photo)
            
            # Also try to set as window icon (for Windows)
            # Save temporary icon file
            icon_path = "temp_app_icon.ico"
            # Create a larger version for ICO file
            large_icon = icon_img.resize((64, 64), Image.Resampling.LANCZOS)
            large_icon.save(icon_path, format='ICO', sizes=[(16,16), (32,32), (64,64)])
            
            # Set icon using iconbitmap (Windows-specific)
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                
        except Exception as e:
            print(f"Could not set icon: {e}")
        
        # Set window class name for better taskbar recognition
        self.root.wm_class("MultiCoordinatesClicker", "Multi Coordinates Clicker")
        
        # Set additional window properties
        self.root.wm_title("🚀 Multi Coordinates Clicker - Enhanced")
        
        # Make window appear in taskbar properly
        self.root.withdraw()  # Hide window temporarily
        self.root.deiconify()  # Show it again to ensure proper taskbar entry
        self.root.lift()  # Bring to front
        self.root.focus_force()  # Give it focus
        
        # Configure modern styling
        self.setup_modern_style()
        self.root.configure(bg=COLORS['light'])
        
        # Initialize variables
        self.is_running = False
        self.current_thread = None
        self.start_time = None
        self.completed_count = 0
        self.auto_refresh_enabled = True
        self.clipboard_refresh_timer = None
        self.last_clipboard_content = ""
        self.sequence_clipboard_content = ""
        
        # Load or create default coordinates
        self.coordinates = self.load_coordinates()
        
        self.setup_ui()
        
        # Start auto-monitoring for clipboard changes
        self.start_auto_refresh()
        
    def load_coordinates(self):
        """Load coordinates from config file or create defaults"""
        try:
            if os.path.exists('coordinates_config.json'):
                with open('coordinates_config.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        
        # Default coordinates
        return [
            {"name": "Position 1", "x": -2658, "y": 934, "press_enter_after_paste": True, "delay_after_action": 0.5},
            {"name": "Position 2", "x": -2002, "y": 985, "press_enter_after_paste": True, "delay_after_action": 0.5},
            {"name": "Position 3", "x": -2644, "y": 1763, "press_enter_after_paste": True, "delay_after_action": 0.5},
            {"name": "Position 4", "x": -1708, "y": 1664, "press_enter_after_paste": True, "delay_after_action": 0.5},
            {"name": "Position 5", "x": -1050, "y": 1721, "press_enter_after_paste": True, "delay_after_action": 0.5},
            {"name": "Position 6", "x": -720, "y": 1040, "press_enter_after_paste": True, "delay_after_action": 0.5},
            {"name": "Position 7", "x": -814, "y": 1699, "press_enter_after_paste": True, "delay_after_action": 0.5},
            {"name": "Position 8", "x": -75, "y": 1766, "press_enter_after_paste": True, "delay_after_action": 0.5}
        ]
    
    def save_coordinates(self):
        """Save coordinates to config file"""
        try:
            with open('coordinates_config.json', 'w') as f:
                json.dump(self.coordinates, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save coordinates: {str(e)}")
    
    def setup_modern_style(self):
        """Configure modern visual styling"""
        style = ttk.Style()
        
        # Configure notebook with better contrast
        style.configure('Modern.TNotebook', background=COLORS['light'], borderwidth=0)
        style.configure('Modern.TNotebook.Tab', padding=[20, 12], font=('Segoe UI', 11, 'bold'),
                       background=COLORS['light'], foreground=COLORS['dark'])
        style.map('Modern.TNotebook.Tab', 
                 background=[('selected', COLORS['info'])],
                 foreground=[('selected', COLORS['dark'])])
        
        # Configure buttons with proper contrast - ensuring all text is dark/black
        style.configure('Success.TButton', font=('Segoe UI', 14, 'bold'), padding=[25, 15],
                       background=COLORS['success'], foreground=COLORS['dark'], borderwidth=2, relief='raised')
        style.configure('Danger.TButton', font=('Segoe UI', 12, 'bold'), padding=[20, 10],
                       background=COLORS['danger'], foreground=COLORS['dark'], borderwidth=2, relief='raised')
        style.configure('Primary.TButton', font=('Segoe UI', 12, 'bold'), padding=[20, 10],
                       background=COLORS['primary'], foreground=COLORS['dark'], borderwidth=2, relief='raised')
        style.configure('Info.TButton', font=('Segoe UI', 12, 'bold'), padding=[20, 10],
                       background=COLORS['info'], foreground=COLORS['dark'], borderwidth=2, relief='raised')
        
        # Map button states for better interaction feedback
        for btn_style in ['Success.TButton', 'Danger.TButton', 'Primary.TButton', 'Info.TButton']:
            style.map(btn_style,
                     relief=[('pressed', 'sunken'), ('active', 'raised')],
                     background=[('active', COLORS['accent'])],
                     foreground=[('active', COLORS['dark'])])
        
        # Configure treeview with readable colors
        style.configure('Modern.Treeview', background=COLORS['bg'], foreground=COLORS['dark'],
                       font=('Segoe UI', 10), fieldbackground=COLORS['bg'], borderwidth=1)
        style.configure('Modern.Treeview.Heading', background=COLORS['light'], foreground=COLORS['dark'],
                       font=('Segoe UI', 11, 'bold'), relief='raised', borderwidth=1)
        
        # Configure entry and other widgets
        style.configure('TEntry', fieldbackground='white', borderwidth=2, relief='solid', foreground=COLORS['dark'])
        style.configure('TLabelframe', background=COLORS['light'], foreground=COLORS['dark'],
                       borderwidth=2, relief='solid')
        style.configure('TLabelframe.Label', background=COLORS['light'], foreground=COLORS['dark'],
                       font=('Segoe UI', 11, 'bold'))
    
    def setup_ui(self):
        """Set up the user interface"""
        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main notebook
        self.notebook = ttk.Notebook(self.root, style='Modern.TNotebook')
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=15)
        
        # Create tabs
        self.setup_main_tab()
        self.setup_settings_tab()
        self.setup_logs_tab()
        
        # Initialize clipboard after all tabs are created
        self.refresh_clipboard()
        # Store initial clipboard content for change detection
        try:
            self.last_clipboard_content = pyperclip.paste()
        except:
            self.last_clipboard_content = ""
    
    def setup_main_tab(self):
        """Set up the main control tab"""
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text="🎯 Main Control")
        main_tab.columnconfigure(0, weight=1)
        main_tab.columnconfigure(1, weight=1)
        main_tab.rowconfigure(1, weight=1)
        
        # Title with better contrast
        title_frame = tk.Frame(main_tab, bg=COLORS['primary'], height=80)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        title_frame.grid_propagate(False)
        title_frame.columnconfigure(0, weight=1)
        
        tk.Label(title_frame, text="🚀 Multi Coordinates Clicker - Enhanced", 
                font=("Segoe UI", 22, "bold"), bg=COLORS['primary'], fg=COLORS['text_on_primary']).grid(row=0, column=0, pady=10)
        tk.Label(title_frame, text="✨ Automated clipboard pasting with adjustable settings ✨",
                font=("Segoe UI", 12), bg=COLORS['primary'], fg=COLORS['text_on_primary']).grid(row=1, column=0)
        
        # Left panel
        left_frame = ttk.LabelFrame(main_tab, text="📋 Clipboard & Control", padding="15")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(15, 8), pady=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Clipboard
        clipboard_header = tk.Frame(left_frame, bg=COLORS['info'], height=35)
        clipboard_header.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        clipboard_header.grid_propagate(False)
        tk.Label(clipboard_header, text="📝 Current Clipboard Content", 
                font=("Segoe UI", 12, "bold"), background=COLORS['info'], foreground=COLORS['dark']).grid(row=0, column=0, padx=10, pady=5)
        
        self.clipboard_text = tk.Text(left_frame, height=8, wrap=tk.WORD, font=("Cascadia Code", 11),
                                     bg=COLORS['bg'], fg=COLORS['dark'], relief='flat', borderwidth=2,
                                     insertbackground=COLORS['dark'], selectbackground=COLORS['info'], selectforeground=COLORS['dark'])
        self.clipboard_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure black text tag for clipboard
        self.clipboard_text.tag_configure("black_text", foreground="#000000", font=("Cascadia Code", 11))
        
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.clipboard_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.clipboard_text.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons with better styling
        control_frame = tk.Frame(left_frame, bg=COLORS['light'])
        control_frame.grid(row=2, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)
        
        # First row of buttons
        ttk.Button(control_frame, text="🔄 Refresh Now", command=self.refresh_clipboard, style='Info.TButton').grid(row=0, column=0, padx=3, pady=3, sticky=(tk.W, tk.E))
        self.auto_refresh_btn = ttk.Button(control_frame, text="⏰ Auto-Monitor: ON", command=self.toggle_auto_refresh, style='Info.TButton')
        self.auto_refresh_btn.grid(row=0, column=1, padx=3, pady=3, sticky=(tk.W, tk.E))
        
        # Second row of buttons
        self.submit_btn = ttk.Button(control_frame, text="🚀 START SEQUENCE", command=self.submit_action, style="Success.TButton")
        self.submit_btn.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky=(tk.W, tk.E))
        self.stop_btn = ttk.Button(control_frame, text="🛑 STOP", command=self.stop_action, style="Danger.TButton", state="disabled")
        self.stop_btn.grid(row=1, column=2, padx=3, pady=3, sticky=(tk.W, tk.E))
        
        # Status
        status_frame = tk.Frame(left_frame, bg=COLORS['light'])
        status_frame.grid(row=3, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_container = tk.Frame(status_frame, bg=COLORS['success'], relief='solid', bd=2)
        self.status_container.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.status_container.columnconfigure(0, weight=1)
        
        self.status_label = tk.Label(self.status_container, text="✅ Ready - Click START SEQUENCE to begin", 
                                    bg=COLORS['success'], fg=COLORS['dark'], font=("Segoe UI", 11, "bold"), pady=8)
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.progress = ttk.Progressbar(status_frame, mode='determinate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=3)
        
        # Right panel
        right_frame = ttk.LabelFrame(main_tab, text="🎯 Configured Coordinates", padding="15")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(8, 15), pady=5)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # Treeview with inline editing
        columns = ("Name", "X", "Y", "Press Enter", "Delay")
        self.coords_tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=12, style='Modern.Treeview')
        
        # Configure column widths and alignment
        column_configs = {
            "Name": {"width": 140, "anchor": "w"},
            "X": {"width": 80, "anchor": "center"},
            "Y": {"width": 80, "anchor": "center"},
            "Press Enter": {"width": 90, "anchor": "center"},
            "Delay": {"width": 70, "anchor": "center"}
        }
        
        for col in columns:
            self.coords_tree.heading(col, text=col)
            self.coords_tree.column(col, 
                                   width=column_configs[col]["width"], 
                                   anchor=column_configs[col]["anchor"],
                                   minwidth=50)
        
        self.coords_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tree_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.coords_tree.yview)
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.coords_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Quick edit buttons
        edit_buttons_frame = tk.Frame(right_frame, bg=COLORS['light'])
        edit_buttons_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        edit_buttons_frame.columnconfigure(0, weight=1)
        edit_buttons_frame.columnconfigure(1, weight=1)
        edit_buttons_frame.columnconfigure(2, weight=1)
        edit_buttons_frame.columnconfigure(3, weight=1)
        edit_buttons_frame.columnconfigure(4, weight=1)
        edit_buttons_frame.columnconfigure(5, weight=1)
        
        # First row - basic operations
        ttk.Button(edit_buttons_frame, text="➕ Add", command=self.quick_add_coordinate, style='Primary.TButton').grid(row=0, column=0, padx=1, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(edit_buttons_frame, text="✏️ Edit", command=self.quick_edit_coordinate, style='Primary.TButton').grid(row=0, column=1, padx=1, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(edit_buttons_frame, text="🎯 Get Pos", command=self.quick_get_position, style='Primary.TButton').grid(row=0, column=2, padx=1, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(edit_buttons_frame, text="🗑️ Delete", command=self.quick_delete_coordinate, style='Danger.TButton').grid(row=0, column=3, padx=1, pady=2, sticky=(tk.W, tk.E))
        
        # Second row - ordering operations
        ttk.Button(edit_buttons_frame, text="⬆️ Up", command=self.move_coordinate_up, style='Info.TButton').grid(row=1, column=0, padx=1, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(edit_buttons_frame, text="⬇️ Down", command=self.move_coordinate_down, style='Info.TButton').grid(row=1, column=1, padx=1, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(edit_buttons_frame, text="🔢 Order", command=self.show_order_dialog, style='Info.TButton').grid(row=1, column=2, padx=1, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(edit_buttons_frame, text="💾 Save", command=self.save_coordinates, style='Success.TButton').grid(row=1, column=3, padx=1, pady=2, sticky=(tk.W, tk.E))
        
        # Quick settings panel with better colors
        quick_settings_frame = ttk.LabelFrame(right_frame, text="⚡ Quick Settings", padding="10")
        quick_settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        quick_settings_frame.columnconfigure(1, weight=1)
        
        # Selected coordinate info with dark text
        tk.Label(quick_settings_frame, text="Selected:", font=("Segoe UI", 10, "bold"), 
                bg=COLORS['light'], fg=COLORS['dark']).grid(row=0, column=0, sticky=tk.W)
        self.selected_coord_label = tk.Label(quick_settings_frame, text="None selected", 
                                           bg=COLORS['light'], fg=COLORS['info'], font=("Segoe UI", 10))
        self.selected_coord_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Quick edit fields labels with dark text
        tk.Label(quick_settings_frame, text="Name:", font=("Segoe UI", 9), 
                bg=COLORS['light'], fg=COLORS['dark']).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.quick_name_var = tk.StringVar()
        self.quick_name_entry = ttk.Entry(quick_settings_frame, textvariable=self.quick_name_var, width=20)
        self.quick_name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        tk.Label(quick_settings_frame, text="X, Y:", font=("Segoe UI", 9), 
                bg=COLORS['light'], fg=COLORS['dark']).grid(row=2, column=0, sticky=tk.W, pady=2)
        coord_frame = tk.Frame(quick_settings_frame, bg=COLORS['light'])
        coord_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        coord_frame.columnconfigure(0, weight=1)
        coord_frame.columnconfigure(2, weight=1)
        
        self.quick_x_var = tk.StringVar()
        self.quick_y_var = tk.StringVar()
        ttk.Entry(coord_frame, textvariable=self.quick_x_var, width=8).grid(row=0, column=0, sticky=(tk.W, tk.E))
        tk.Label(coord_frame, text=",", bg=COLORS['light'], fg=COLORS['dark']).grid(row=0, column=1, padx=5)
        ttk.Entry(coord_frame, textvariable=self.quick_y_var, width=8).grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        tk.Label(quick_settings_frame, text="Enter:", font=("Segoe UI", 9), 
                bg=COLORS['light'], fg=COLORS['dark']).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.quick_enter_var = tk.BooleanVar()
        ttk.Checkbutton(quick_settings_frame, variable=self.quick_enter_var).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        tk.Label(quick_settings_frame, text="Delay:", font=("Segoe UI", 9), 
                bg=COLORS['light'], fg=COLORS['dark']).grid(row=4, column=0, sticky=tk.W, pady=2)
        self.quick_delay_var = tk.StringVar()
        ttk.Entry(quick_settings_frame, textvariable=self.quick_delay_var, width=10).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Update button
        ttk.Button(quick_settings_frame, text="💾 Update Selected", command=self.update_selected_coordinate, style='Success.TButton').grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Bind tree selection
        self.coords_tree.bind('<<TreeviewSelect>>', self.on_coordinate_select)
        
        self.populate_coordinates()
    
    def setup_settings_tab(self):
        """Set up the settings tab with adjustable coordinates"""
        settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(settings_tab, text="⚙️ Settings")
        settings_tab.columnconfigure(0, weight=1)
        settings_tab.rowconfigure(1, weight=1)
        
        # Title in settings tab with dark text
        tk.Label(settings_tab, text="⚙️ Coordinate Settings", font=("Segoe UI", 18, "bold"),
                bg=COLORS['light'], fg=COLORS['dark']).grid(row=0, column=0, pady=20)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(settings_tab, text="Edit Coordinates", padding="15")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=10)
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.rowconfigure(0, weight=1)
        
        # Coordinate editor
        self.setup_coordinate_editor(settings_frame)
    
    def setup_coordinate_editor(self, parent):
        """Set up the coordinate editor"""
        # Editor treeview
        editor_frame = tk.Frame(parent)
        editor_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        
        columns = ("Name", "X", "Y", "Press Enter", "Delay")
        self.editor_tree = ttk.Treeview(editor_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.editor_tree.heading(col, text=col)
            self.editor_tree.column(col, width=150, anchor="center")
        
        self.editor_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        editor_scrollbar = ttk.Scrollbar(editor_frame, orient="vertical", command=self.editor_tree.yview)
        editor_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.editor_tree.configure(yscrollcommand=editor_scrollbar.set)
        
        # Buttons
        button_frame = tk.Frame(parent)
        button_frame.grid(row=1, column=0, pady=20)
        
        ttk.Button(button_frame, text="➕ Add Coordinate", command=self.add_coordinate, style='Primary.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="✏️ Edit Selected", command=self.edit_coordinate, style='Primary.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Selected", command=self.delete_coordinate, style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="💾 Save Changes", command=self.save_changes, style='Success.TButton').grid(row=0, column=3, padx=5)
        
        self.populate_editor()
    
    def setup_logs_tab(self):
        """Set up the logs tab"""
        logs_tab = ttk.Frame(self.notebook)
        self.notebook.add(logs_tab, text="📋 Logs")
        logs_tab.columnconfigure(0, weight=1)
        logs_tab.rowconfigure(1, weight=1)
        
        # Header in logs tab with dark text
        header_frame = ttk.Frame(logs_tab)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        header_frame.columnconfigure(0, weight=1)
        
        tk.Label(header_frame, text="📋 Activity Logs", font=("Segoe UI", 16, "bold"),
                bg=COLORS['light'], fg=COLORS['dark']).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(header_frame, text="Clear Logs", command=self.clear_logs, style='Primary.TButton').grid(row=0, column=1)
        
        # Logs
        logs_frame = ttk.Frame(logs_tab)
        logs_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)
        
        self.logs_text = tk.Text(logs_frame, wrap=tk.WORD, font=("Consolas", 9), state=tk.DISABLED,
                                bg='white', fg='#000000', insertbackground='black')
        self.logs_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        logs_scrollbar = ttk.Scrollbar(logs_frame, orient="vertical", command=self.logs_text.yview)
        logs_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.logs_text.configure(yscrollcommand=logs_scrollbar.set)
        
        self.log_message("Application started", "INFO")
    
    def start_auto_refresh(self):
        """Start automatic clipboard monitoring for new content"""
        def check_clipboard():
            if self.auto_refresh_enabled:
                self.check_clipboard_for_changes()
                # Schedule next check in 2 seconds for less intrusive monitoring
                self.clipboard_refresh_timer = self.root.after(2000, check_clipboard)
        
        # Start the first check after 2 seconds
        self.clipboard_refresh_timer = self.root.after(2000, check_clipboard)
    
    def stop_auto_refresh(self):
        """Stop automatic clipboard refresh"""
        self.auto_refresh_enabled = False
        if self.clipboard_refresh_timer:
            self.root.after_cancel(self.clipboard_refresh_timer)
    
    def toggle_auto_refresh(self):
        """Toggle automatic clipboard monitoring on/off"""
        if self.auto_refresh_enabled:
            self.stop_auto_refresh()
            self.auto_refresh_btn.config(text="⏰ Auto-Monitor: OFF")
            self.update_status("🔄 Clipboard monitoring disabled", "warning")
            self.log_message("Clipboard monitoring disabled", "INFO")
        else:
            self.auto_refresh_enabled = True
            self.start_auto_refresh()
            self.auto_refresh_btn.config(text="⏰ Auto-Monitor: ON")
            self.update_status("🔄 Clipboard monitoring enabled", "success")
            self.log_message("Clipboard monitoring enabled", "INFO")
    
    def populate_coordinates(self):
        """Populate main coordinates tree"""
        # Clear existing items
        for item in self.coords_tree.get_children():
            self.coords_tree.delete(item)
        
        # Configure tag for proper text display
        self.coords_tree.tag_configure('coordinate_row', foreground='#000000', font=('Segoe UI', 10))
        
        # Add coordinates with proper formatting
        for i, coord in enumerate(self.coordinates):
            # Ensure all values are properly formatted
            name = str(coord.get("name", f"Position {i+1}"))[:15]  # Limit name length
            x_val = str(coord.get("x", 0))
            y_val = str(coord.get("y", 0))
            enter_val = "Yes" if coord.get("press_enter_after_paste", False) else "No"
            delay_val = f"{coord.get('delay_after_action', 1.0):.1f}s"
            
            self.coords_tree.insert("", "end", values=(
                name, x_val, y_val, enter_val, delay_val
            ), tags=('coordinate_row',))
        
        # Force refresh
        self.coords_tree.update_idletasks()
    
    def populate_editor(self):
        """Populate editor tree"""
        for item in self.editor_tree.get_children():
            self.editor_tree.delete(item)
        
        self.editor_tree.tag_configure('black_text', foreground='black')

        for coord in self.coordinates:
            self.editor_tree.insert("", "end", values=(
                coord["name"], coord["x"], coord["y"],
                "Yes" if coord["press_enter_after_paste"] else "No",
                coord['delay_after_action']
            ), tags=('black_text',))
    
    def add_coordinate(self):
        """Add new coordinate"""
        self.edit_coordinate_dialog()
    
    def edit_coordinate(self):
        """Edit selected coordinate"""
        selection = self.editor_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a coordinate to edit.")
            return
        
        index = self.editor_tree.index(selection[0])
        self.edit_coordinate_dialog(index)
    
    def edit_coordinate_dialog(self, index=None):
        """Show coordinate edit dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Coordinate" if index is not None else "Add Coordinate")
        dialog.geometry("400x320")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=COLORS['light'])

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Fields Frame
        fields_frame = tk.Frame(dialog, bg=COLORS['light'])
        fields_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Fields
        ttk.Label(fields_frame, text="Name:", background=COLORS['light'], foreground=COLORS['dark']).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_var = tk.StringVar(value=self.coordinates[index]["name"] if index is not None else "New Position")
        ttk.Entry(fields_frame, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(fields_frame, text="X Coordinate:", background=COLORS['light'], foreground=COLORS['dark']).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        x_var = tk.StringVar(value=str(self.coordinates[index]["x"]) if index is not None else "100")
        ttk.Entry(fields_frame, textvariable=x_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(fields_frame, text="Y Coordinate:", background=COLORS['light'], foreground=COLORS['dark']).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        y_var = tk.StringVar(value=str(self.coordinates[index]["y"]) if index is not None else "100")
        ttk.Entry(fields_frame, textvariable=y_var, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(fields_frame, text="Press Enter:", background=COLORS['light'], foreground=COLORS['dark']).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        enter_var = tk.BooleanVar(value=self.coordinates[index]["press_enter_after_paste"] if index is not None else True)
        ttk.Checkbutton(fields_frame, variable=enter_var).grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(fields_frame, text="Delay (sec):", background=COLORS['light'], foreground=COLORS['dark']).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        delay_var = tk.StringVar(value=str(self.coordinates[index]["delay_after_action"]) if index is not None else "0.5")
        ttk.Entry(fields_frame, textvariable=delay_var, width=30).grid(row=4, column=1, padx=10, pady=5)
        
        # Get current mouse position button
        def get_mouse_pos():
            try:
                dialog.withdraw()
                result = messagebox.askokcancel("Get Position", 
                    "1. Position your mouse where you want to capture\n"
                    "2. Click OK\n" 
                    "3. DO NOT move mouse for 3 seconds\n\n"
                    "The position will be captured automatically.")
                
                if result:
                    time.sleep(3)
                    x, y = pyautogui.position()
                    x_var.set(str(x))
                    y_var.set(str(y))
                    dialog.deiconify()
                    messagebox.showinfo("Success", f"Position captured: ({x}, {y})")
                else:
                    dialog.deiconify()
            except Exception as e:
                dialog.deiconify()
                messagebox.showerror("Error", f"Failed to capture position: {str(e)}")
        
        ttk.Button(fields_frame, text="🎯 Get Current Mouse Position", command=get_mouse_pos, style='Info.TButton').grid(row=5, column=0, columnspan=2, pady=10)
        
        # Buttons Frame
        button_frame = tk.Frame(dialog, bg=COLORS['light'])
        button_frame.pack(pady=10)

        # Buttons
        def save_coordinate():
            try:
                coord = {
                    "name": name_var.get(),
                    "x": int(x_var.get()),
                    "y": int(y_var.get()),
                    "press_enter_after_paste": enter_var.get(),
                    "delay_after_action": float(delay_var.get())
                }
                
                if index is not None:
                    self.coordinates[index] = coord
                else:
                    self.coordinates.append(coord)
                
                self.populate_editor()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for coordinates and delay.")
        
        ttk.Button(button_frame, text="💾 Save", command=save_coordinate, style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=dialog.destroy, style='Danger.TButton').grid(row=0, column=1, padx=5)
    
    def delete_coordinate(self):
        """Delete selected coordinate"""
        selection = self.editor_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a coordinate to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this coordinate?"):
            index = self.editor_tree.index(selection[0])
            del self.coordinates[index]
            self.populate_editor()
    
    def save_changes(self):
        """Save all changes"""
        self.save_coordinates()
        self.populate_coordinates()
        messagebox.showinfo("Saved", "Coordinates saved successfully!")
        self.log_message("Coordinates configuration saved", "INFO")
    
    def on_coordinate_select(self, event):
        """Handle coordinate selection in main tab"""
        selection = self.coords_tree.selection()
        if selection:
            index = self.coords_tree.index(selection[0])
            coord = self.coordinates[index]
            
            # Update quick settings panel
            self.selected_coord_label.config(text=f"{coord['name']} (#{index+1})")
            self.quick_name_var.set(coord["name"])
            self.quick_x_var.set(str(coord["x"]))
            self.quick_y_var.set(str(coord["y"]))
            self.quick_enter_var.set(coord["press_enter_after_paste"])
            self.quick_delay_var.set(str(coord["delay_after_action"]))
        else:
            self.selected_coord_label.config(text="None selected")
            self.quick_name_var.set("")
            self.quick_x_var.set("")
            self.quick_y_var.set("")
            self.quick_enter_var.set(False)
            self.quick_delay_var.set("")
    
    def quick_add_coordinate(self):
        """Quick add new coordinate"""
        new_coord = {
            "name": f"Position {len(self.coordinates) + 1}",
            "x": 100,
            "y": 100,
            "press_enter_after_paste": True,
            "delay_after_action": 0.5
        }
        self.coordinates.append(new_coord)
        self.populate_coordinates()
        self.save_coordinates()
        # Select the new coordinate
        children = self.coords_tree.get_children()
        if children:
            self.coords_tree.selection_set(children[-1])
            self.coords_tree.focus(children[-1])
        self.log_message(f"Added new coordinate: {new_coord['name']}", "INFO")
    
    def quick_edit_coordinate(self):
        """Quick edit selected coordinate"""
        selection = self.coords_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a coordinate to edit.")
            return
        
        index = self.coords_tree.index(selection[0])
        self.edit_coordinate_dialog(index)
    
    def quick_get_position(self):
        """Quick get mouse position for selected coordinate"""
        def get_position():
            try:
                # Hide main window temporarily
                self.root.withdraw()
                
                # Show instruction dialog
                result = messagebox.askokcancel("Get Position", 
                    "1. Position your mouse where you want to capture\n"
                    "2. Click OK\n"
                    "3. DO NOT move mouse for 3 seconds\n\n"
                    "The position will be captured automatically.")
                
                if result:
                    time.sleep(3)
                    x, y = pyautogui.position()
                    
                    # Update the quick settings fields
                    self.quick_x_var.set(str(x))
                    self.quick_y_var.set(str(y))
                    
                    # Show main window again
                    self.root.deiconify()
                    self.root.lift()
                    
                    # Update status and log
                    self.update_status(f"✅ Position captured: ({x}, {y})", "success")
                    self.log_message(f"Captured position: ({x}, {y})", "INFO")
                    
                    # If a coordinate is selected, show message about updating
                    selection = self.coords_tree.selection()
                    if selection:
                        messagebox.showinfo("Position Captured", 
                            f"Position ({x}, {y}) captured!\n\n"
                            "Click 'Update Selected' to save this position to the selected coordinate.")
                    else:
                        messagebox.showinfo("Position Captured", 
                            f"Position ({x}, {y}) captured!\n\n"
                            "You can now use 'Add' to create a new coordinate with this position.")
                else:
                    # Show main window again if cancelled
                    self.root.deiconify()
                    self.root.lift()
                    
            except Exception as e:
                # Make sure window is shown again
                self.root.deiconify()
                self.root.lift()
                messagebox.showerror("Error", f"Failed to capture position: {str(e)}")
                self.log_message(f"Position capture error: {str(e)}", "ERROR")
        
        # Run in thread to avoid blocking
        thread = threading.Thread(target=get_position)
        thread.daemon = True
        thread.start()
    
    def quick_delete_coordinate(self):
        """Quick delete selected coordinate"""
        selection = self.coords_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a coordinate to delete.")
            return
        
        index = self.coords_tree.index(selection[0])
        coord_name = self.coordinates[index]["name"]
        
        if messagebox.askyesno("Confirm Delete", f"Delete '{coord_name}'?"):
            del self.coordinates[index]
            self.populate_coordinates()
            self.save_coordinates()
            self.log_message(f"Deleted coordinate: {coord_name}", "INFO")
            
            # Clear quick settings
            self.selected_coord_label.config(text="None selected")
            self.quick_name_var.set("")
            self.quick_x_var.set("")
            self.quick_y_var.set("")
            self.quick_enter_var.set(False)
            self.quick_delay_var.set("")
    
    def move_coordinate_up(self):
        """Move selected coordinate up in the list"""
        selection = self.coords_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a coordinate to move.")
            return
        
        index = self.coords_tree.index(selection[0])
        if index == 0:
            messagebox.showinfo("Cannot Move", "This coordinate is already at the top.")
            return
        
        # Swap coordinates
        self.coordinates[index], self.coordinates[index-1] = self.coordinates[index-1], self.coordinates[index]
        self.populate_coordinates()
        self.save_coordinates()
        
        # Re-select the moved coordinate
        children = self.coords_tree.get_children()
        if index-1 < len(children):
            self.coords_tree.selection_set(children[index-1])
            self.coords_tree.focus(children[index-1])
        
        self.update_status(f"✅ Moved '{self.coordinates[index-1]['name']}' up", "success")
        self.log_message(f"Moved coordinate up: {self.coordinates[index-1]['name']}", "INFO")
    
    def move_coordinate_down(self):
        """Move selected coordinate down in the list"""
        selection = self.coords_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a coordinate to move.")
            return
        
        index = self.coords_tree.index(selection[0])
        if index == len(self.coordinates) - 1:
            messagebox.showinfo("Cannot Move", "This coordinate is already at the bottom.")
            return
        
        # Swap coordinates
        self.coordinates[index], self.coordinates[index+1] = self.coordinates[index+1], self.coordinates[index]
        self.populate_coordinates()
        self.save_coordinates()
        
        # Re-select the moved coordinate
        children = self.coords_tree.get_children()
        if index+1 < len(children):
            self.coords_tree.selection_set(children[index+1])
            self.coords_tree.focus(children[index+1])
        
        self.update_status(f"✅ Moved '{self.coordinates[index+1]['name']}' down", "success")
        self.log_message(f"Moved coordinate down: {self.coordinates[index+1]['name']}", "INFO")
    
    def show_order_dialog(self):
        """Show dialog to manually set coordinate order"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Reorder Coordinates")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=COLORS['light'])
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=COLORS['primary'], height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="🔢 Reorder Coordinates", font=("Segoe UI", 16, "bold"),
                bg=COLORS['primary'], fg=COLORS['text_on_primary']).pack(expand=True)
        
        # Instructions
        tk.Label(dialog, text="Drag and drop or use buttons to reorder:", 
                bg=COLORS['light'], fg=COLORS['dark'], font=("Segoe UI", 10)).pack(pady=5)
        
        # Listbox for reordering
        list_frame = tk.Frame(dialog, bg=COLORS['light'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        order_listbox = tk.Listbox(list_frame, font=("Segoe UI", 10), height=12,
                                  bg='white', fg=COLORS['dark'], selectbackground=COLORS['info'])
        order_listbox.pack(side='left', fill='both', expand=True)
        
        order_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=order_listbox.yview)
        order_scrollbar.pack(side='right', fill='y')
        order_listbox.configure(yscrollcommand=order_scrollbar.set)
        
        # Populate listbox
        for i, coord in enumerate(self.coordinates):
            order_listbox.insert(tk.END, f"{i+1}. {coord['name']} ({coord['x']}, {coord['y']})")
        
        # Buttons for moving
        button_frame = tk.Frame(dialog, bg=COLORS['light'])
        button_frame.pack(pady=10)
        
        def move_up():
            try:
                index = order_listbox.curselection()[0]
                if index > 0:
                    # Swap in list and coordinates
                    order_listbox.insert(index-1, order_listbox.get(index))
                    order_listbox.delete(index+1)
                    order_listbox.selection_set(index-1)
                    
                    self.coordinates[index], self.coordinates[index-1] = self.coordinates[index-1], self.coordinates[index]
            except IndexError:
                messagebox.showwarning("No Selection", "Please select an item to move.")
        
        def move_down():
            try:
                index = order_listbox.curselection()[0]
                if index < order_listbox.size() - 1:
                    # Swap in list and coordinates
                    order_listbox.insert(index+2, order_listbox.get(index))
                    order_listbox.delete(index)
                    order_listbox.selection_set(index+1)
                    
                    self.coordinates[index], self.coordinates[index+1] = self.coordinates[index+1], self.coordinates[index]
            except IndexError:
                messagebox.showwarning("No Selection", "Please select an item to move.")
        
        def save_order():
            self.populate_coordinates()
            self.save_coordinates()
            self.update_status("✅ Coordinate order saved", "success")
            self.log_message("Coordinate order updated", "INFO")
            dialog.destroy()
        
        ttk.Button(button_frame, text="⬆️ Move Up", command=move_up, style='Info.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="⬇️ Move Down", command=move_down, style='Info.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="💾 Save Order", command=save_order, style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=dialog.destroy, style='Danger.TButton').pack(side='left', padx=5)
    
    def update_selected_coordinate(self):
        """Update the selected coordinate with quick settings values"""
        selection = self.coords_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a coordinate to update.")
            return
        
        try:
            index = self.coords_tree.index(selection[0])
            
            # Validate inputs
            name = self.quick_name_var.get().strip()
            x = int(self.quick_x_var.get())
            y = int(self.quick_y_var.get())
            delay = float(self.quick_delay_var.get())
            
            if not name:
                messagebox.showerror("Invalid Input", "Name cannot be empty.")
                return
            
            # Update coordinate
            self.coordinates[index] = {
                "name": name,
                "x": x,
                "y": y,
                "press_enter_after_paste": self.quick_enter_var.get(),
                "delay_after_action": delay
            }
            
            self.populate_coordinates()
            self.save_coordinates()
            
            # Re-select the updated coordinate
            children = self.coords_tree.get_children()
            if index < len(children):
                self.coords_tree.selection_set(children[index])
                self.coords_tree.focus(children[index])
            
            self.update_status(f"✅ Updated '{name}'", "success")
            self.log_message(f"Updated coordinate: {name} at ({x}, {y})", "INFO")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for coordinates and delay.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update coordinate: {str(e)}")
    
    def check_clipboard_for_changes(self):
        """Check if clipboard content has changed and update if so"""
        try:
            clipboard_content = pyperclip.paste()
            
            # Skip if clipboard contains JSON (likely from our own config)
            if clipboard_content.strip().startswith('{') or clipboard_content.strip().startswith('['):
                try:
                    import json
                    json.loads(clipboard_content)
                    # If it's valid JSON, probably our config - skip
                    return
                except:
                    pass  # Not JSON, continue normally
            
            # More robust change detection - avoid false positives
            if clipboard_content != self.last_clipboard_content:
                # Don't update if new content is empty and we had content before
                # (this prevents losing content due to clipboard clearing)
                if not clipboard_content.strip() and self.last_clipboard_content.strip():
                    return
                
                # Don't update if the change is just whitespace differences
                if clipboard_content.strip() == self.last_clipboard_content.strip() and self.last_clipboard_content:
                    return
                
                # Only update if there's a meaningful change
                if len(clipboard_content.strip()) > 0 or not self.last_clipboard_content:
                    self.last_clipboard_content = clipboard_content
                    self.update_clipboard_display(clipboard_content)
                
        except Exception as e:
            # Silently handle clipboard access errors to avoid spam
            pass

    def update_clipboard_display(self, clipboard_content):
        """Update the clipboard display with new content"""
        try:
            self.clipboard_text.config(state='normal')
            self.clipboard_text.delete(1.0, tk.END)
            
            # Add timestamp and content
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            header = f"🕒 Content updated: {timestamp}\n" + "="*50 + "\n"
            
            # Show full clipboard content (no truncation)
            display_content = clipboard_content
            
            self.clipboard_text.insert(1.0, header + display_content)
            
            # Configure proper text styling
            self.clipboard_text.tag_add("black_text", "1.0", tk.END)
            self.clipboard_text.tag_configure("black_text", foreground="#000000", font=("Cascadia Code", 11))
            self.clipboard_text.config(state='disabled', fg='#000000')
            
            # Show success message briefly
            self.update_status("✅ Clipboard content updated", "success")
            self.log_message(f"Clipboard content updated - {len(clipboard_content)} characters", "INFO")
            
        except Exception as e:
            self.update_status(f"❌ Clipboard Display Error: {str(e)}", "error")
            self.log_message(f"Clipboard display error: {str(e)}", "ERROR")

    def refresh_clipboard(self):
        """Manually refresh clipboard display (force update)"""
        try:
            clipboard_content = pyperclip.paste()
            
            # Skip if clipboard contains JSON (likely from our own config)
            if clipboard_content.strip().startswith('{') or clipboard_content.strip().startswith('['):
                try:
                    import json
                    json.loads(clipboard_content)
                    # If it's valid JSON, probably our config - get real clipboard
                    clipboard_content = "No text in clipboard (contains data/JSON)"
                except:
                    pass  # Not JSON, continue normally
            
            # Force update regardless of whether content changed
            self.last_clipboard_content = clipboard_content
            self.clipboard_text.config(state='normal')
            self.clipboard_text.delete(1.0, tk.END)
            
            # Add timestamp and content
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            header = f"🕒 Manually refreshed: {timestamp}\n" + "="*50 + "\n"
            
            # Show full clipboard content (no truncation)
            display_content = clipboard_content
            
            self.clipboard_text.insert(1.0, header + display_content)
            
            # Configure proper text styling
            self.clipboard_text.tag_add("black_text", "1.0", tk.END)
            self.clipboard_text.tag_configure("black_text", foreground="#000000", font=("Cascadia Code", 11))
            self.clipboard_text.config(state='disabled', fg='#000000')
            
            # Show success message briefly
            self.update_status("✅ Clipboard manually refreshed", "success")
            self.log_message(f"Clipboard manually refreshed - {len(clipboard_content)} characters", "INFO")
        except Exception as e:
            self.update_status(f"❌ Clipboard Error: {str(e)}", "error")
            self.log_message(f"Clipboard refresh error: {str(e)}", "ERROR")
    
    def update_status(self, message, status_type="info"):
        """Update status with colors"""
        colors = {'success': COLORS['success'], 'error': COLORS['danger'], 'warning': COLORS['warning'], 'info': COLORS['info']}
        color = colors.get(status_type, COLORS['secondary'])
        self.status_container.config(bg=color)
        self.status_label.config(text=message, bg=color, fg=COLORS['dark'])
    
    def log_message(self, message, level="INFO"):
        """Add message to logs"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        # Only log if logs_text widget exists (logs tab has been created)
        if hasattr(self, 'logs_text') and self.logs_text:
            self.logs_text.config(state=tk.NORMAL)
            self.logs_text.insert(tk.END, log_entry)
            self.logs_text.see(tk.END)
            self.logs_text.config(state=tk.DISABLED)
    
    def clear_logs(self):
        """Clear all logs"""
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.delete(1.0, tk.END)
        self.logs_text.config(state=tk.DISABLED)
        self.log_message("Logs cleared", "INFO")
    
    def submit_action(self):
        """Start the sequence"""
        if self.is_running:
            return
        
        try:
            self.sequence_clipboard_content = pyperclip.paste()
            if not self.sequence_clipboard_content.strip():
                messagebox.showwarning("Empty Clipboard", "Please copy some text first.")
                return
        except Exception as e:
            messagebox.showerror("Clipboard Error", f"Error: {str(e)}")
            return
        
        self.is_running = True
        self.submit_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.start_time = time.time()
        self.completed_count = 0
        
        self.log_message(f"Starting sequence with {len(self.coordinates)} coordinates", "INFO")
        
        self.current_thread = threading.Thread(target=self.execute_sequence)
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def stop_action(self):
        """Stop the sequence"""
        self.is_running = False
        self.submit_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.update_status("🛑 Sequence stopped", "warning")
        self.log_message("Sequence stopped by user", "WARNING")
    
    def execute_sequence(self):
        """Execute the pasting sequence"""
        try:
            total_coords = len(self.coordinates)
            self.progress.config(maximum=total_coords)
            
            # Initial delay
            for i in range(3, 0, -1):
                if not self.is_running:
                    return
                self.update_status(f"⏳ Starting in {i} seconds...", "warning")
                time.sleep(1)
            
            # Process each coordinate
            for index, coord in enumerate(self.coordinates):
                if not self.is_running:
                    return
                
                self.update_status(f"🔄 Processing {coord['name']} ({index+1}/{total_coords})", "info")
                self.log_message(f"Processing {coord['name']} at ({coord['x']}, {coord['y']})", "INFO")
                
                # Move and click
                pyautogui.moveTo(coord["x"], coord["y"], duration=0.5)
                pyautogui.click(coord["x"], coord["y"])
                time.sleep(0.2)
                
                # Restore clipboard content before pasting
                pyperclip.copy(self.sequence_clipboard_content)
                time.sleep(0.1) # Brief pause for clipboard to settle

                # Paste
                pyautogui.hotkey('ctrl', 'v')
                
                # Press Enter if configured
                if coord["press_enter_after_paste"]:
                    time.sleep(0.1)
                    pyautogui.press('enter')
                    self.log_message(f"Pressed Enter after pasting at {coord['name']}", "DEBUG")
                
                self.completed_count += 1
                self.progress.config(value=index + 1)
                self.log_message(f"Completed {coord['name']}", "SUCCESS")
                
                # Wait before next
                if index < total_coords - 1:
                    delay = coord["delay_after_action"]
                    for i in range(int(delay * 10)):
                        if not self.is_running:
                            return
                        time.sleep(0.1)
            
            if self.is_running:
                total_time = int(time.time() - self.start_time)
                self.update_status(f"✅ Completed! {total_coords} locations in {total_time}s", "success")
                self.log_message(f"Sequence completed in {total_time} seconds", "SUCCESS")
        
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", "error")
            self.log_message(f"Error: {str(e)}", "ERROR")
        
        finally:
            self.is_running = False
            self.submit_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

def main():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
    
    root = tk.Tk()
    app = MultiCoordinatesClicker(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Handle window close event
    def on_closing():
        app.stop_auto_refresh()
        # Clean up temporary icon file
        try:
            if os.path.exists("temp_app_icon.ico"):
                os.remove("temp_app_icon.ico")
        except:
            pass
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 