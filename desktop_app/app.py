"""
Jesus Projekt Erfurt - Birthday Monitoring
Desktop Application Launcher
Runs the Flask web app in a native webview window - exact same UI as run.bat
"""
import os
import sys
import shutil
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
    # PyInstaller extracts data files to _MEIPASS
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


def get_logo_image(size=(150, 80)):
    logo_path = os.path.join(APP_DIR, 'logo.jpg')
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            img.thumbnail(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            pass
    if hasattr(sys, '_MEIPASS'):
        logo_path = os.path.join(sys._MEIPASS, 'logo.jpg')
        if os.path.exists(logo_path):
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

        self.logo_img = get_logo_image((160, 160))
        if self.logo_img:
            tk.Label(card, image=self.logo_img, bg=WHITE).pack(pady=(35, 15))
        else:
            tk.Label(card, text="🎂", font=("Segoe UI Emoji", 56),
                    bg=WHITE, fg=PRIMARY).pack(pady=(35, 15))

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


def start_flask_server(port, db_path, uploads_dir):
    """Start the Flask server in a background thread"""
    # Add webapp dir to path so 'app' module can be found
    if WEBAPP_DIR not in sys.path:
        sys.path.insert(0, WEBAPP_DIR)

    # Set environment variables
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    os.environ['UPLOADS_DIR'] = uploads_dir

    # Import and run Flask app
    from app import create_app
    flask_app = create_app()
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
            time.sleep(0.1)
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

        # Start Flask server in background thread
        loading.update_status("Starting server...", 70)
        server_thread = threading.Thread(
            target=start_flask_server,
            args=(port, db_path, uploads_dir),
            daemon=True
        )
        server_thread.start()

        # Wait for server
        if not wait_for_server(port, timeout=15):
            loading.close()
            messagebox.showerror("Jesus Projekt Erfurt",
                               "Failed to start the server. Please try again.")
            return

        loading.update_status("Ready!", 100)
        time.sleep(0.3)
        loading.close()

        # Open in webview (native window with web content)
        url = f'http://127.0.0.1:{port}'

        import webview

        # Determine icon path
        icon_path = get_icon_path()

        window = webview.create_window(
            title='Jesus Projekt Erfurt - Birthday Monitoring',
            url=url,
            width=1300,
            height=800,
            min_size=(900, 600),
            resizable=True,
            text_select=True,
            easy_drag=False,
            confirm_close=False
        )

        # Show first-run notice
        if is_first_run:
            def show_notice():
                webview.windows[0].evaluate_js(
                    f"alert('Welcome!\\n\\nDefault admin account created:\\n\\nUsername: admin\\nPassword: admin123\\n\\nPlease change your password after logging in.')"
                )
            window.events.loaded += show_notice

        webview.start()

    except Exception as e:
        error_msg = f"Failed to start application:\n\n{str(e)}"
        try:
            messagebox.showerror("Jesus Projekt Erfurt - Error", error_msg)
        except Exception:
            print(error_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
