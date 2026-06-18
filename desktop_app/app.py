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

# Database locations
EXE_DB_PATH = os.path.join(APP_DIR, 'birthday_monitoring.db')
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Jesus Projekt Erfurt')
APPDATA_DB_PATH = os.path.join(APPDATA_DIR, 'birthday_monitoring.db')

UPLOADS_DIR = os.path.join(APP_DIR, 'uploads')
APPDATA_UPLOADS = os.path.join(APPDATA_DIR, 'uploads')

LOGO_URL = 'https://jesus-projekt-erfurt.de/wp-content/uploads/2017/03/Jesus-Projekt-Erfurt-Logo.jpg'
LOCAL_LOGO = os.path.join(APP_DIR, 'logo.jpg')


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


def get_logo_path():
    if os.path.exists(LOCAL_LOGO):
        return LOCAL_LOGO
    try:
        import urllib.request
        urllib.request.urlretrieve(LOGO_URL, LOCAL_LOGO)
        return LOCAL_LOGO
    except Exception:
        return None


class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Jesus Projekt Erfurt")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

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

        main = tk.Frame(self.root, bg=BG)
        main.pack(expand=True, fill='both')

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=400, height=320)

        # Logo
        logo_img = get_logo_path()
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

        self.status_label = tk.Label(card, text="Loading...", font=("Segoe UI", 10),
                                     bg=WHITE, fg=TEXT)
        self.status_label.pack(pady=(0, 10))

        self.progress = ttk.Progressbar(card, length=300, mode='determinate')
        self.progress.pack(pady=(0, 20))

    def update_status(self, text, progress=None):
        self.status_label.config(text=text)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update_idletasks()
        self.root.update()


# Color scheme (same as main_app)
PRIMARY = '#ff8e00'
PRIMARY_DARK = '#e67e00'
TEXT = '#666666'
WHITE = '#ffffff'
BG = '#f7f7f7'


def show_error_and_exit(message, details=""):
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
    try:
        root = tk.Tk()
        loading = LoadingScreen(root)

        def do_loading():
            try:
                import time

                loading.update_status("Initializing application...", 10)
                time.sleep(0.3)

                loading.update_status("Checking database location...", 30)
                time.sleep(0.3)

                db_path, db_dir, uploads_dir = get_db_path()
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                os.makedirs(uploads_dir, exist_ok=True)

                loading.update_status("Loading modules...", 50)
                time.sleep(0.3)

                loading.update_status("Starting application...", 80)
                time.sleep(0.3)

                loading.update_status("Ready!", 100)
                time.sleep(0.5)

                root.destroy()

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
