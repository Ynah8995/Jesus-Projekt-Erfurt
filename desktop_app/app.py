"""
Jesus Projekt Erfurt - Birthday Monitoring Desktop Application
Main entry point with loading screen
"""
import os
import sys
import traceback
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


def get_db_path():
    """Try to create db in exe folder, fallback to AppData"""
    if can_write_to(APP_DIR):
        return EXE_DB_PATH, APP_DIR, UPLOADS_DIR
    else:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        os.makedirs(APPDATA_UPLOADS, exist_ok=True)
        return APPDATA_DB_PATH, APPDATA_DIR, APPDATA_UPLOADS


def get_icon_path():
    """Get the icon file path"""
    if getattr(sys, 'frozen', False):
        # When running as exe, look for icon in the same folder
        icon_path = os.path.join(APP_DIR, 'app.ico')
        if os.path.exists(icon_path):
            return icon_path
        # Also check _MEIPASS for PyInstaller
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'app.ico')
    # When running as script
    return os.path.join(APP_DIR, 'app.ico')


class LoadingScreen:
    """Nice looking loading screen shown on startup"""

    def __init__(self, root):
        self.root = root
        self.root.title("Jesus Projekt Erfurt")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Set icon
        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # Center on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2
        self.root.geometry(f"500x350+{x}+{y}")

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


def show_error_and_exit(message, details=""):
    """Show error dialog and exit"""
    try:
        root = tk.Tk()
        root.withdraw()
        full_message = message
        if details:
            full_message += "\n\nDetails:\n" + details
        messagebox.showerror("Jesus Projekt Erfurt - Error", full_message)
        root.destroy()
    except Exception:
        print(message)
        if details:
            print(details)
    sys.exit(1)


def run_app():
    """Main entry point"""
    try:
        # Show loading screen
        root = tk.Tk()
        loading = LoadingScreen(root)

        def do_loading():
            try:
                import time

                # Step 1: Initialize
                loading.update_status("Initializing application...", 10)
                time.sleep(0.3)

                # Step 2: Check database location
                loading.update_status("Checking database location...", 30)
                time.sleep(0.3)

                db_path, db_dir, uploads_dir = get_db_path()
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                os.makedirs(uploads_dir, exist_ok=True)

                # Step 3: Load modules
                loading.update_status("Loading modules...", 50)
                time.sleep(0.3)

                # Step 4: Create app
                loading.update_status("Starting application...", 80)
                time.sleep(0.3)

                # Step 5: Ready
                loading.update_status("Ready!", 100)
                time.sleep(0.5)

                # Close loading screen
                root.destroy()

                # Import and start main app
                from main_app import LoginWindow
                main_root = tk.Tk()
                LoginWindow(main_root, db_path, db_dir, uploads_dir)
                main_root.mainloop()

            except Exception as e:
                root.destroy()
                show_error_and_exit("Failed to start application", traceback.format_exc())

        root.after(100, do_loading)
        root.mainloop()

    except Exception as e:
        show_error_and_exit("Unexpected error", traceback.format_exc())


if __name__ == '__main__':
    run_app()
