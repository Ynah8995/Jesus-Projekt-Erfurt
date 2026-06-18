"""
Jesus Projekt Erfurt - Birthday Monitoring
Desktop Application Launcher

Starts the Flask web app and opens it in a native desktop window.
Uses pywebview for a true desktop app experience with the same web UI.
"""
import os
import sys
import threading
import time
import webbrowser
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Get the directory where the exe is located
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    # PyInstaller extracts to _MEIPASS at runtime
    if hasattr(sys, '_MEIPASS'):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = APP_DIR
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = APP_DIR

# Database locations
EXE_DB_PATH = os.path.join(APP_DIR, 'birthday_monitoring.db')
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Jesus Projekt Erfurt')
APPDATA_DB_PATH = os.path.join(APPDATA_DIR, 'birthday_monitoring.db')

UPLOADS_DIR = os.path.join(APP_DIR, 'uploads')
APPDATA_UPLOADS = os.path.join(APPDATA_DIR, 'uploads')

# Logo
LOCAL_LOGO = os.path.join(APP_DIR, 'logo.jpg')
LOGO_URL = 'https://jesus-projekt-erfurt.de/wp-content/uploads/2017/03/Jesus-Projekt-Erfurt-Logo.jpg'

# Color scheme
PRIMARY = '#ff8e00'
TEXT = '#666666'
WHITE = '#ffffff'
BG = '#f7f7f7'


def can_write_to(directory):
    try:
        test_file = os.path.join(directory, '.write_test')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except (OSError, PermissionError):
        return False


def get_db_path():
    if can_write_to(APP_DIR):
        return EXE_DB_PATH, APP_DIR, UPLOADS_DIR
    else:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        os.makedirs(APPDATA_UPLOADS, exist_ok=True)
        return APPDATA_DB_PATH, APPDATA_DIR, APPDATA_UPLOADS


def get_icon_path():
    icon_path = os.path.join(APP_DIR, 'app.ico')
    if os.path.exists(icon_path):
        return icon_path
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'app.ico')
    return icon_path


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def download_logo():
    if os.path.exists(LOCAL_LOGO):
        return LOCAL_LOGO
    try:
        import urllib.request
        urllib.request.urlretrieve(LOGO_URL, LOCAL_LOGO)
        return LOCAL_LOGO
    except Exception:
        return None


class LoadingScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jesus Projekt Erfurt")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.overrideredirect(True)

        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 400) // 2
        self.root.geometry(f"500x400+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(expand=True, fill='both')

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=400, height=320)

        logo_img = download_logo()
        if logo_img:
            try:
                from PIL import Image, ImageTk
                img = Image.open(logo_img)
                img.thumbnail((150, 150))
                self.logo_photo = ImageTk.PhotoImage(img)
                tk.Label(card, image=self.logo_photo, bg=WHITE).pack(pady=(30, 10))
            except Exception:
                tk.Label(card, text="🎂", font=("Segoe UI Emoji", 48), bg=WHITE, fg=PRIMARY).pack(pady=(30, 10))
        else:
            tk.Label(card, text="🎂", font=("Segoe UI Emoji", 48), bg=WHITE, fg=PRIMARY).pack(pady=(30, 10))

        tk.Label(card, text="Jesus Projekt Erfurt", font=("Segoe UI", 18, "bold"),
                bg=WHITE, fg=PRIMARY).pack()
        tk.Label(card, text="Birthday Monitoring", font=("Segoe UI", 11),
                bg=WHITE, fg=TEXT).pack(pady=(0, 20))

        self.status_label = tk.Label(card, text="Starting server...", font=("Segoe UI", 10),
                                     bg=WHITE, fg=TEXT)
        self.status_label.pack(pady=(0, 10))

        self.progress = ttk.Progressbar(card, length=300, mode='determinate')
        self.progress.pack(pady=(0, 20))

    def update_status(self, text, progress=None):
        if not self.root.winfo_exists():
            return
        try:
            self.status_label.config(text=text)
            if progress is not None:
                self.progress['value'] = progress
            self.root.update_idletasks()
            self.root.update()
        except Exception:
            pass

    def close(self):
        try:
            self.root.destroy()
        except Exception:
            pass


def start_flask_server(port, db_path, uploads_dir, base_dir):
    """Start the Flask server in a separate thread"""
    # Add the base directory to path so 'app' module can be found
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    # Set environment variables for database
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    os.environ['UPLOADS_DIR'] = uploads_dir

    # Import the Flask app
    from app import create_app
    flask_app = create_app()

    # Run the server (no reloader, no debug for exe)
    flask_app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)


def wait_for_server(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(('127.0.0.1', port))
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.2)
    return False


def run_app():
    try:
        loading = LoadingScreen()
        loading.update_status("Initializing...", 10)
        time.sleep(0.3)

        loading.update_status("Checking database location...", 25)
        db_path, db_dir, uploads_dir = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)
        time.sleep(0.3)

        loading.update_status("Setting up server...", 40)
        port = find_free_port()
        time.sleep(0.2)

        loading.update_status("Starting server...", 60)
        # Use BASE_DIR (which is _MEIPASS when frozen) for finding the app module
        server_thread = threading.Thread(
            target=start_flask_server,
            args=(port, db_path, uploads_dir, BASE_DIR),
            daemon=True
        )
        server_thread.start()

        loading.update_status("Waiting for server...", 80)
        if not wait_for_server(port, timeout=30):
            loading.close()
            messagebox.showerror(
                "Jesus Projekt Erfurt",
                "Failed to start the server. Please try again."
            )
            return

        loading.update_status("Opening application...", 95)
        time.sleep(0.5)

        loading.close()

        url = f'http://127.0.0.1:{port}'

        try:
            # Try to use pywebview for native window experience
            import webview
            window = webview.create_window(
                'Jesus Projekt Erfurt - Birthday Monitoring',
                url,
                width=1200,
                height=750,
                min_size=(900, 600),
                resizable=True,
                text_select=True,
                easy_drag=False
            )
            webview.start()
        except ImportError:
            # Fallback to default browser
            webbrowser.open(url)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

    except Exception as e:
        try:
            messagebox.showerror("Jesus Projekt Erfurt - Error", str(e))
        except Exception:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    run_app()
