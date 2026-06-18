"""
Jesus Projekt Erfurt - Birthday Monitoring
Desktop Application - Main entry point
Pure tkinter - no browser, no webview, no server
"""
import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from config import (PRIMARY, TEXT, WHITE, BG, FONT_FAMILY, FONT_EMOJI,
                    APP_DIR, get_db_path, get_icon_path, get_logo_image,
                    apply_window_icon, center_window, t)


class LoadingScreen:
    """Splash screen shown during application startup"""

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

        # White card
        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=440, height=360)

        # Official Jesus Projekt Erfurt logo
        self.logo_img = get_logo_image((240, 120))
        if self.logo_img:
            tk.Label(card, image=self.logo_img, bg=WHITE).pack(pady=(30, 15))
        else:
            tk.Label(card, text="🎂", font=(FONT_EMOJI, 56),
                    bg=WHITE, fg=PRIMARY).pack(pady=(30, 15))

        tk.Label(card, text="Jesus Projekt Erfurt", font=(FONT_FAMILY, 20, "bold"),
                bg=WHITE, fg=PRIMARY).pack()
        tk.Label(card, text="Birthday Monitoring", font=(FONT_FAMILY, 12),
                bg=WHITE, fg=TEXT).pack(pady=(0, 25))

        self.status_label = tk.Label(card, text="Starting...", font=(FONT_FAMILY, 10),
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


def ensure_first_run_admin(db_path):
    """Create default admin on first run (when no users exist)"""
    from datetime import datetime
    from models import init_db, User

    engine, session = init_db(db_path)
    existing = session.query(User).first()
    if existing:
        session.close()
        return False
    admin = User(username='admin', email='admin@jesus-projekt.de',
                first_name='Admin', last_name='User', role='admin',
                is_active=True, language='en')
    admin.set_password('admin123')
    admin.created_at = datetime.utcnow()
    session.add(admin)
    session.commit()
    session.close()
    return True


def main():
    try:
        loading = LoadingScreen()
        loading.update_status("Starting...", 30)
        time.sleep(0.3)

        db_path, db_dir, uploads_dir = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)

        loading.update_status("Setting up...", 60)
        is_first_run = ensure_first_run_admin(db_path)

        loading.update_status("Ready!", 100)
        time.sleep(0.3)
        loading.close()

        from windows import LoginWindow
        root = tk.Tk()
        LoginWindow(root, db_path, db_dir, uploads_dir)

        if is_first_run:
            root.after(500, lambda: messagebox.showinfo(
                "Jesus Projekt Erfurt",
                "Welcome! Default admin account created:\n\n"
                "Username: admin\n"
                "Password: admin123\n\n"
                "Please change your password after logging in."
            ))

        root.mainloop()
    except Exception as e:
        error_msg = f"Failed to start application:\n\n{str(e)}"
        try:
            messagebox.showerror("Jesus Projekt Erfurt - Error", error_msg)
        except Exception:
            print(error_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
