"""
Jesus Projekt Erfurt - Birthday Monitoring Desktop Application
Main entry point with loading screen
"""
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Get the directory where the exe is located
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine database location
# First try: same folder as exe
EXE_DB_PATH = os.path.join(APP_DIR, 'birthday_monitoring.db')

# Fallback: AppData/Roaming/Jesus Projekt Erfurt
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Jesus Projekt Erfurt')
APPDATA_DB_PATH = os.path.join(APPDATA_DIR, 'birthday_monitoring.db')

UPLOADS_DIR = os.path.join(APP_DIR, 'uploads')
APPDATA_UPLOADS = os.path.join(APPDATA_DIR, 'uploads')


def get_db_path():
    """Try to create db in exe folder, fallback to AppData"""
    if can_write_to(APP_DIR):
        return EXE_DB_PATH, APP_DIR, UPLOADS_DIR
    else:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        os.makedirs(APPDATA_UPLOADS, exist_ok=True)
        return APPDATA_DB_PATH, APPDATA_DIR, APPDATA_UPLOADS


def can_write_to(directory):
    """Test if we can write to the given directory"""
    try:
        test_file = os.path.join(directory, '.write_test')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except (OSError, PermissionError):
        return False


class LoadingScreen:
    """Nice looking loading screen shown on startup"""

    def __init__(self, root):
        self.root = root
        self.root.title("Jesus Projekt Erfurt")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Center on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2
        self.root.geometry(f"500x350+{x}+{y}")

        # Remove window decorations for a cleaner look (optional)
        # self.root.overrideredirect(True)

        # Background
        self.root.configure(bg='#ff8e00')

        # Logo
        self.logo_label = tk.Label(
            root,
            text="🎂",
            font=("Segoe UI Emoji", 48),
            bg='#ff8e00',
            fg='white'
        )
        self.logo_label.pack(pady=(40, 10))

        # App name
        self.title_label = tk.Label(
            root,
            text="Jesus Projekt Erfurt",
            font=("Segoe UI", 22, "bold"),
            bg='#ff8e00',
            fg='white'
        )
        self.title_label.pack()

        # Subtitle
        self.subtitle_label = tk.Label(
            root,
            text="Birthday Monitoring",
            font=("Segoe UI", 12),
            bg='#ff8e00',
            fg='white'
        )
        self.subtitle_label.pack(pady=(0, 30))

        # Status label
        self.status_label = tk.Label(
            root,
            text="Loading...",
            font=("Segoe UI", 10),
            bg='#ff8e00',
            fg='white'
        )
        self.status_label.pack(pady=(0, 10))

        # Progress bar
        self.progress = ttk.Progressbar(
            root,
            length=400,
            mode='determinate',
            style="orange.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(0, 20))

        # Style for progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("orange.Horizontal.TProgressbar",
                        background='white',
                        troughcolor='#e67e00',
                        borderwidth=0,
                        lightcolor='white',
                        darkcolor='white')

    def update_status(self, text, progress=None):
        """Update loading status text and progress"""
        self.status_label.config(text=text)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update_idletasks()
        self.root.update()


def run_loading_and_start():
    """Show loading screen, then start the app"""
    root = tk.Tk()
    loading = LoadingScreen(root)

    def do_loading():
        # Step 1: Initialize
        loading.update_status("Initializing application...", 10)
        import time
        time.sleep(0.3)

        # Step 2: Check database
        loading.update_status("Checking database...", 30)
        time.sleep(0.3)

        db_path, db_dir, uploads_dir = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)

        # Step 3: Load models
        loading.update_status("Loading modules...", 50)
        time.sleep(0.3)

        # Step 4: Create app
        loading.update_status("Starting application...", 80)
        time.sleep(0.3)

        # Step 5: Ready
        loading.update_status("Ready!", 100)
        time.sleep(0.5)

        # Close loading screen and start main app
        root.destroy()

        # Import here to avoid slowing down loading screen
        from main_app import MainApp
        main_root = tk.Tk()
        MainApp(main_root, db_path, db_dir, uploads_dir)
        main_root.mainloop()

    # Run loading in main thread (fast operations only)
    root.after(100, do_loading)
    root.mainloop()


if __name__ == '__main__':
    run_loading_and_start()
