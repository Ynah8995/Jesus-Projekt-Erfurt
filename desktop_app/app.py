"""
Jesus Projekt Erfurt - Birthday Monitoring
Desktop Application - Flask web app in native WebView2 window
Shows the EXACT same UI as the development version (run.bat)
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

# Web app is bundled at the root of the bundle (via --add-data 'webapp/app;app')
# So 'app' is at BASE_DIR/app/
# We add BASE_DIR to sys.path so 'import app' works
WEBAPP_DIR = BASE_DIR

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
        bundled = os.path.join(sys._MEIPASS, 'app.ico')
        if os.path.exists(bundled):
            return bundled
    if os.path.exists(os.path.join(APP_DIR, 'app.ico')):
        return os.path.join(APP_DIR, 'app.ico')
    return os.path.join(APP_DIR, 'app.ico')


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def get_logo_image(size=(200, 100)):
    """Load the official Jesus Projekt Erfurt logo"""
    # Try bundled first
    if hasattr(sys, '_MEIPASS'):
        bundled = os.path.join(sys._MEIPASS, 'logo.jpg')
        if os.path.exists(bundled):
            try:
                img = Image.open(bundled)
                img.thumbnail(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception:
                pass
    # Try APP_DIR
    local = os.path.join(APP_DIR, 'logo.jpg')
    if os.path.exists(local):
        try:
            img = Image.open(local)
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
    """Splash screen shown while server starts"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jesus Projekt Erfurt")
        self.root.geometry("500x420")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.overrideredirect(True)

        apply_window_icon(self.root)
        center_window(self.root, 500, 420)

        self.build_ui()
        self.closed = False

    def build_ui(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(expand=True, fill='both')

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=440, height=360)

        # Official Jesus Projekt Erfurt logo
        self.logo_img = get_logo_image((240, 120))
        if self.logo_img:
            tk.Label(card, image=self.logo_img, bg=WHITE).pack(pady=(30, 15))
        else:
            tk.Label(card, text="🎂", font=("Segoe UI Emoji", 56),
                    bg=WHITE, fg=PRIMARY).pack(pady=(30, 15))

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


def start_flask_server(port, db_path, uploads_dir, error_event):
    """Start the Flask server in a background thread"""
    try:
        # Make sure WEBAPP_DIR is at the front of sys.path
        if WEBAPP_DIR not in sys.path:
            sys.path.insert(0, WEBAPP_DIR)
        else:
            # Move it to the front
            sys.path.remove(WEBAPP_DIR)
            sys.path.insert(0, WEBAPP_DIR)

        # Set environment variables
        os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
        os.environ['UPLOADS_DIR'] = uploads_dir

        # Import and run Flask app
        from app import create_app
        flask_app = create_app()
        flask_app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    except Exception as e:
        import traceback
        error_event.set()
        # Write error to a file for debugging
        try:
            with open(os.path.join(APP_DIR, 'server_error.log'), 'w') as f:
                f.write(f"Server error: {e}\n{traceback.format_exc()}")
        except:
            pass


def wait_for_server(port, timeout=20):
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

    # Make sure WEBAPP_DIR is at the front of sys.path
    if WEBAPP_DIR not in sys.path:
        sys.path.insert(0, WEBAPP_DIR)

    # Import models from the webapp
    from app.models import Base, User

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
        time.sleep(0.3)

        # Setup database
        db_path, db_dir, uploads_dir = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)

        # Create first admin if needed
        loading.update_status("Setting up...", 50)
        is_first_run = create_first_admin_if_needed(db_path)

        # Find free port
        port = find_free_port()
        error_event = threading.Event()

        # Start Flask server in background thread
        loading.update_status("Starting server...", 70)
        server_thread = threading.Thread(
            target=start_flask_server,
            args=(port, db_path, uploads_dir, error_event),
            daemon=True
        )
        server_thread.start()

        # Wait for server
        loading.update_status("Waiting for server...", 85)
        if not wait_for_server(port, timeout=20):
            loading.close()
            # Check for error log
            error_log = os.path.join(APP_DIR, 'server_error.log')
            error_msg = "Failed to start the server. Please try again."
            if os.path.exists(error_log):
                try:
                    with open(error_log, 'r') as f:
                        error_content = f.read()
                    error_msg = f"Server error:\n\n{error_content[:500]}"
                except:
                    pass
            messagebox.showerror("Jesus Projekt Erfurt", error_msg)
            return

        loading.update_status("Opening application...", 95)
        time.sleep(0.3)
        loading.close()

        # Open in webview (native window with WebView2)
        url = f'http://127.0.0.1:{port}'

        import webview

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
                try:
                    webview.windows[0].evaluate_js(
                        "alert('Welcome!\\n\\nDefault admin account created:\\n\\nUsername: admin\\nPassword: admin123\\n\\nPlease change your password after logging in.')"
                    )
                except:
                    pass
            try:
                window.events.loaded += show_notice
            except:
                pass

        webview.start()

    except Exception as e:
        error_msg = f"Failed to start application:\n\n{str(e)}"
        import traceback
        error_msg += f"\n\n{traceback.format_exc()}"
        try:
            messagebox.showerror("Jesus Projekt Erfurt - Error", error_msg)
        except Exception:
            print(error_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
