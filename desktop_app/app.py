"""
Jesus Projekt Erfurt - Birthday Monitoring
Desktop Application - Main entry point
"""
import os
import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time

from config import (PRIMARY, TEXT, WHITE, BG, FONT_FAMILY, FONT_LOGO_EMOJI,
                    APP_DIR, get_db_path, get_icon_path, get_logo_image,
                    apply_window_icon, center_window, t)


class LoadingScreen:
    """Splash screen shown during application startup"""

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

        # White card
        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=420, height=340)

        # Logo
        self.logo_img = get_logo_image((160, 160))
        if self.logo_img:
            logo_label = tk.Label(card, image=self.logo_img, bg=WHITE)
            logo_label.pack(pady=(35, 15))
        else:
            tk.Label(card, text="🎂", font=(FONT_LOGO_EMOJI, 56),
                    bg=WHITE, fg=PRIMARY).pack(pady=(35, 15))

        tk.Label(card, text="Jesus Projekt Erfurt", font=(FONT_FAMILY, 20, "bold"),
                bg=WHITE, fg=PRIMARY).pack()
        tk.Label(card, text="Birthday Monitoring", font=(FONT_FAMILY, 12),
                bg=WHITE, fg=TEXT).pack(pady=(0, 25))

        self.status_label = tk.Label(card, text="Loading...", font=(FONT_FAMILY, 10),
                                     bg=WHITE, fg=TEXT)
        self.status_label.pack(pady=(0, 8))

        # Progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("orange.Horizontal.TProgressbar",
                       background=PRIMARY,
                       troughcolor='#e0e0e0',
                       bordercolor='#e0e0e0',
                       lightcolor=PRIMARY,
                       darkcolor=PRIMARY)

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
    """Create default admin user on first run (when no users exist)"""
    from datetime import datetime
    from models import init_db, User

    engine, session = init_db(db_path)

    # Check if any user exists
    existing = session.query(User).first()
    if existing:
        session.close()
        return False  # Not first run

    # Create default admin
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
    return True  # First run, admin created


def main():
    """Main entry point"""
    try:
        # Show loading screen
        loading = LoadingScreen()
        loading.update_status("Starting...", 30)

        # Setup database (fast)
        db_path, db_dir, uploads_dir = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(uploads_dir, exist_ok=True)

        # Create default admin on first run
        loading.update_status("Setting up...", 60)
        is_first_run = ensure_first_run_admin(db_path)

        loading.update_status("Ready!", 100)
        loading.root.update()

        # Minimal delay for visual feedback
        time.sleep(0.3)
        loading.close()

        # Open login window
        from windows import LoginWindow
        root = tk.Tk()
        LoginWindow(root, db_path, db_dir, uploads_dir)

        # Show first-run notice after login window is ready
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
