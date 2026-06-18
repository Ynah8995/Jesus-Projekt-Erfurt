"""
Jesus Projekt Erfurt - Birthday Monitoring
Desktop Application Launcher
Runs the Flask web app and opens it in a native window.
"""
import os
import sys
import shutil
import subprocess
import threading
import time
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Get the directory where the exe is located
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    if hasattr(sys, '_MEIPASS'):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = APP_DIR
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = APP_DIR

# Web app is bundled in the exe
WEBAPP_DIR = os.path.join(BASE_DIR, 'webapp')

# Database locations
EXE_DB_PATH = os.path.join(APP_DIR, 'birthday_monitoring.db')
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Jesus Projekt Erfurt')
APPDATA_DB_PATH = os.path.join(APPDATA_DIR, 'birthday_monitoring.db')

UPLOADS_DIR = os.path.join(APP_DIR, 'uploads')
APPDATA_UPLOADS = os.path.join(APPDATA_DIR, 'uploads')

# Colors
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
    if hasattr(sys, '_MEIPASS'):
        meipass_icon = os.path.join(sys._MEIPASS, 'app.ico')
        if os.path.exists(meipass_icon):
            return meipass_icon
    icon_path = os.path.join(APP_DIR, 'app.ico')
    if os.path.exists(icon_path):
        return icon_path
    return icon_path


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def get_logo_path():
    """Get the local logo file path"""
    # Check _MEIPASS first (bundled in exe)
    if hasattr(sys, '_MEIPASS'):
        bundled = os.path.join(sys._MEIPASS, 'logo.jpg')
        if os.path.exists(bundled):
            return bundled
    # Check APP_DIR
    local = os.path.join(APP_DIR, 'logo.jpg')
    if os.path.exists(local):
        return local
    return None


def get_logo_image(size=(150, 80)):
    """Load and resize the logo image"""
    logo_path = get_logo_path()
    if logo_path:
        try:
            img = Image.open(logo_path)
            img.thumbnail(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            pass
    return None


def apply_window_icon(window):
    try:
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            window.iconbitmap(icon_path)
    except Exception:
        pass


def center_window(window, width, height):
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


class LoadingScreen:
    """Splash screen shown while the server starts"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jesus Projekt Erfurt")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.overrideredirect(True)

        apply_window_icon(self.root)
        center_window(self.root, 500, 400)

        self.build_ui()
        self.closed = False

    def build_ui(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(expand=True, fill='both')

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=420, height=340)

        # Logo - use the official Jesus Projekt Erfurt logo
        self.logo_img = get_logo_image((200, 100))
        if self.logo_img:
            tk.Label(card, image=self.logo_img, bg=WHITE).pack(pady=(30, 10))
        else:
            tk.Label(card, text="🎂", font=("Segoe UI Emoji", 56),
                    bg=WHITE, fg=PRIMARY).pack(pady=(30, 10))

        tk.Label(card, text="Jesus Projekt Erfurt", font=("Segoe UI", 20, "bold"),
                bg=WHITE, fg=PRIMARY).pack()
        tk.Label(card, text="Birthday Monitoring", font=("Segoe UI", 12),
                bg=WHITE, fg=TEXT).pack(pady=(0, 25))

        self.status_label = tk.Label(card, text="Starting...", font=("Segoe UI", 10),
                                     bg=WHITE, fg=TEXT)
        self.status_label.pack(pady=(0, 8))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("orange.Horizontal.TProgressbar",
                       background=PRIMARY, troughcolor='#e0e0e0',
                       bordercolor='#e0e0e0', lightcolor=PRIMARY, darkcolor=PRIMARY)

        self.progress = ttk.Progressbar(card, length=320, mode='determinate',
                                       style="orange.Horizontal.TProgressbar")
        self.progress.pack(pady=(0, 20))

    def update_status(self, text, progress=None):
        if self.closed:
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
        self.closed = True
        try:
            self.root.destroy()
        except Exception:
            pass


def start_flask_server(port, db_path, uploads_dir, ready_event):
    """Start the Flask server in a background thread"""
    try:
        # Add webapp dir to path
        if WEBAPP_DIR not in sys.path:
            sys.path.insert(0, WEBAPP_DIR)

        # Set environment variables
        os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
        os.environ['UPLOADS_DIR'] = uploads_dir

        # Import and run Flask app
        from app import create_app
        flask_app = create_app()

        # Signal that server is ready
        ready_event.set()

        flask_app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    except Exception as e:
        ready_event.set()
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()


def wait_for_server(port, timeout=15):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(('127.0.0.1', port))
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.1)
    return False


def find_chrome_exe():
    """Find Chrome or Edge executable for app mode"""
    paths = [
        os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%ProgramFiles%\Microsoft\Edge\Application\msedge.exe'),
        os.path.expandvars(r'%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe'),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def open_native_window(url):
    """Open URL in a native-looking window"""
    # Try Chrome/Edge app mode (gives native window without browser UI)
    chrome = find_chrome_exe()
    if chrome:
        try:
            subprocess.Popen([
                chrome,
                f'--app={url}',
                '--window-size=1300,800',
                '--window-position=100,100',
            ])
            return True
        except Exception:
            pass
    return False


def create_first_admin_if_needed(db_path):
    """Create default admin on first run"""
    from datetime import datetime
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base, User

    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    existing = session.query(User).first()
    if existing:
        session.close()
        return False

    admin = User(
        username='admin',
        email='admin@jesus-projekt.de',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_active=True,
        language='en'
    )
    admin.set_password('admin123')
    admin.created_at = datetime.utcnow()
    session.add(admin)
    session.commit()
    session.close()
    return True


def main():
    """Main entry point"""
    try:
        # Show loading screen
        loading = LoadingScreen()
        loading.update_status("Starting...", 20)

        # Setup database
        db_path, db_dir, uploads_dir = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)

        # Create first admin if needed
        loading.update_status("Setting up...", 50)
        is_first_run = create_first_admin_if_needed(db_path)

        # Find free port
        port = find_free_port()
        ready_event = threading.Event()

        # Start Flask server in background thread
        loading.update_status("Starting server...", 70)
        server_thread = threading.Thread(
            target=start_flask_server,
            args=(port, db_path, uploads_dir, ready_event),
            daemon=True
        )
        server_thread.start()

        # Wait for server to be ready
        loading.update_status("Waiting for server...", 85)
        if not wait_for_server(port, timeout=20):
            loading.close()
            messagebox.showerror("Jesus Projekt Erfurt",
                               "Failed to start the server. Please try again.")
            return

        loading.update_status("Opening application...", 95)
        time.sleep(0.3)
        loading.close()

        # Open in native window
        url = f'http://127.0.0.1:{port}'

        # Try Chrome/Edge app mode first (native window)
        if not open_native_window(url):
            # Fallback to default browser
            import webbrowser
            webbrowser.open(url)

        # Keep the process alive while server runs
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    except Exception as e:
        error_msg = f"Failed to start application:\n\n{str(e)}"
        try:
            messagebox.showerror("Jesus Projekt Erfurt - Error", error_msg)
        except Exception:
            print(error_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
