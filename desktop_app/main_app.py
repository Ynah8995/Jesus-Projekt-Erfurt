"""
Jesus Projekt Erfurt - Birthday Monitoring Desktop Application
Matches the web version (run.bat) design exactly.
"""
import os
import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime, date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
import uuid
import csv

from models import User, Client, Settings, init_db

# Color scheme - matches web version CSS
PRIMARY = '#ff8e00'
PRIMARY_DARK = '#e67e00'
PRIMARY_HOVER = '#cc7a00'
SECONDARY = '#2ea3f2'
BG = '#f7f7f7'
BG_LIGHT = '#fafafa'
TEXT = '#666666'
TEXT_DARK = '#333333'
WHITE = '#ffffff'
DARK = '#222222'
SUCCESS = '#28a745'
DANGER = '#dc3545'
WARNING = '#ffc107'
INFO = '#17a2b8'

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

# Logo URLs (same as web version)
LOGO_URL = 'https://jesus-projekt-erfurt.de/wp-content/uploads/2017/03/Jesus-Projekt-Erfurt-Logo.jpg'
LOCAL_LOGO = os.path.join(APP_DIR, 'logo.jpg')


# ==================== TRANSLATIONS (same as web version) ====================

TRANSLATIONS = {
    'en': {
        'app_name': 'Jesus Projekt Erfurt',
        'app_subtitle': 'Birthday Monitoring',
        'login': 'Login',
        'logout': 'Logout',
        'username': 'Username',
        'password': 'Password',
        'login_error': 'Invalid username or password.',
        'account_deactivated': 'Account is deactivated.',
        'dashboard': 'Dashboard',
        'clients': 'Clients',
        'add_client': 'Add Client',
        'edit_client': 'Edit Client',
        'delete_client': 'Delete Client',
        'select_month': 'Select Month',
        'all_months': 'All Months',
        'birthday_celebrants': 'Birthday Celebrants',
        'no_celebrants': 'No birthday celebrants found for this month.',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'address': 'Address',
        'phone': 'Phone',
        'email': 'Email',
        'birthday': 'Birthday',
        'age': 'Age',
        'privacy_signed': 'Privacy Signed',
        'photo_permission': 'Photo Permission',
        'yes': 'Yes',
        'no': 'No',
        'save': 'Save',
        'cancel': 'Cancel',
        'actions': 'Actions',
        'edit': 'Edit',
        'delete': 'Delete',
        'confirm_delete': 'Confirm Deletion',
        'admin_password': 'Admin Password',
        'back': 'Back',
        'total_clients': 'Total Clients',
        'month_celebrants': 'Month Celebrants',
        'welcome': 'Welcome',
        'language': 'Language',
        'home': 'Home',
        'january': 'January', 'february': 'February', 'march': 'March', 'april': 'April',
        'may': 'May', 'june': 'June', 'july': 'July', 'august': 'August',
        'september': 'September', 'october': 'October', 'november': 'November', 'december': 'December',
        'client_added': 'Client added successfully.',
        'client_updated': 'Client updated successfully.',
        'client_deleted': 'Client deleted successfully.',
        'incorrect_password': 'Incorrect admin password.',
        'required_field': 'This field is required.',
        'send_greetings': 'Send Birthday Greetings',
        'greeting_subject': 'Happy Birthday, {name}!',
        'greeting_message': 'Dear {name},\n\nWishing you a wonderful birthday! May this special day bring you joy, happiness, and all the things you love.\n\nFrom all of us at Jesus Projekt Erfurt, we wish you a fantastic year ahead!\n\nWith warm regards,\nJesus Projekt Erfurt Team',
        'send_to_all': 'Send to All',
        'sending': 'Sending...',
        'greetings_sent': 'Birthday greetings sent successfully!',
        'greeting_error': 'Error sending greetings. Please try again.',
        'no_email_clients': 'No clients with email addresses found.',
        'recipients': 'Recipients',
        'subject': 'Subject',
        'message': 'Message',
        'mail_not_configured': 'Email is not configured. Please go to Settings to configure email.',
        'user_management': 'User Management',
        'add_user': 'Add User',
        'edit_user': 'Edit User',
        'users': 'Users',
        'role': 'Role',
        'admin': 'Admin',
        'staff': 'Staff',
        'status': 'Status',
        'active': 'Active',
        'inactive': 'Inactive',
        'last_login': 'Last Login',
        'profile': 'Profile',
        'profile_picture': 'Profile Picture',
        'new_password': 'New Password',
        'leave_blank_no_change': 'Leave blank to keep current password',
        'admin_actions': 'Admin Actions',
        'reset_password': 'Reset Password',
        'confirm_reset_password': 'Are you sure you want to reset this user\'s password?',
        'confirm_delete_user': 'Are you sure you want to delete this user?',
        'cannot_delete_self': 'You cannot delete your own account.',
        'user_added': 'User added successfully.',
        'user_updated': 'User updated successfully.',
        'user_deleted': 'User deleted successfully.',
        'user_not_found': 'User not found.',
        'username_exists': 'Username already exists.',
        'email_exists': 'Email already exists.',
        'edit_profile': 'Edit Profile',
        'settings': 'Settings',
        'email_settings': 'Email Settings',
        'smtp_server': 'SMTP Server',
        'smtp_port': 'SMTP Port',
        'use_tls': 'Use TLS',
        'email_address': 'Email Address',
        'app_password': 'App Password',
        'sender_address': 'Sender Address',
        'settings_saved': 'Settings saved successfully.',
    },
    'de': {
        'app_name': 'Jesus Projekt Erfurt',
        'app_subtitle': 'Geburtstagsmonitoring',
        'login': 'Anmelden',
        'logout': 'Abmelden',
        'username': 'Benutzername',
        'password': 'Passwort',
        'login_error': 'Ungültiger Benutzername oder Passwort.',
        'account_deactivated': 'Konto ist deaktiviert.',
        'dashboard': 'Dashboard',
        'clients': 'Kunden',
        'add_client': 'Kunde hinzufügen',
        'edit_client': 'Kunde bearbeiten',
        'delete_client': 'Kunde löschen',
        'select_month': 'Monat wählen',
        'all_months': 'Alle Monate',
        'birthday_celebrants': 'Geburtstagsfeiernde',
        'no_celebrants': 'Keine Geburtstagskinder für diesen Monat gefunden.',
        'first_name': 'Vorname',
        'last_name': 'Nachname',
        'address': 'Adresse',
        'phone': 'Telefon',
        'email': 'E-Mail',
        'birthday': 'Geburtstag',
        'age': 'Alter',
        'privacy_signed': 'Datenschutz',
        'photo_permission': 'Fotoerlaubnis',
        'yes': 'Ja',
        'no': 'Nein',
        'save': 'Speichern',
        'cancel': 'Abbrechen',
        'actions': 'Aktionen',
        'edit': 'Bearbeiten',
        'delete': 'Löschen',
        'confirm_delete': 'Löschen bestätigen',
        'admin_password': 'Admin-Passwort',
        'back': 'Zurück',
        'total_clients': 'Kunden gesamt',
        'month_celebrants': 'Monats-Geburtstagskinder',
        'welcome': 'Willkommen',
        'language': 'Sprache',
        'home': 'Startseite',
        'january': 'Januar', 'february': 'Februar', 'march': 'März', 'april': 'April',
        'may': 'Mai', 'june': 'Juni', 'july': 'Juli', 'august': 'August',
        'september': 'September', 'october': 'Oktober', 'november': 'November', 'december': 'Dezember',
        'client_added': 'Kunde erfolgreich hinzugefügt.',
        'client_updated': 'Kunde erfolgreich aktualisiert.',
        'client_deleted': 'Kunde erfolgreich gelöscht.',
        'incorrect_password': 'Falsches Admin-Passwort.',
        'required_field': 'Dieses Feld ist erforderlich.',
        'send_greetings': 'Geburtstagsgrüße senden',
        'greeting_subject': 'Alles Gute zum Geburtstag, {name}!',
        'greeting_message': 'Liebe/r {name},\n\nWir wünschen Dir einen wundervollen Geburtstag! Möge dieser besondere Tag Dir Freude, Glück und all die Dinge bringen, die Du liebst.\n\nVon uns allen bei Jesus Projekt Erfurt wünschen wir Dir ein fantastisches Jahr!\n\nHerzliche Grüße,\nJesus Projekt Erfurt Team',
        'send_to_all': 'An alle senden',
        'sending': 'Wird gesendet...',
        'greetings_sent': 'Geburtstagsgrüße erfolgreich gesendet!',
        'greeting_error': 'Fehler beim Senden. Bitte versuchen Sie es erneut.',
        'no_email_clients': 'Keine Kunden mit E-Mail-Adressen gefunden.',
        'recipients': 'Empfänger',
        'subject': 'Betreff',
        'message': 'Nachricht',
        'mail_not_configured': 'E-Mail ist nicht konfiguriert. Bitte gehen Sie zu Einstellungen.',
        'user_management': 'Benutzerverwaltung',
        'add_user': 'Benutzer hinzufügen',
        'edit_user': 'Benutzer bearbeiten',
        'users': 'Benutzer',
        'role': 'Rolle',
        'admin': 'Administrator',
        'staff': 'Mitarbeiter',
        'status': 'Status',
        'active': 'Aktiv',
        'inactive': 'Inaktiv',
        'last_login': 'Letzte Anmeldung',
        'profile': 'Profil',
        'profile_picture': 'Profilbild',
        'new_password': 'Neues Passwort',
        'leave_blank_no_change': 'Leer lassen, um aktuelles Passwort zu behalten',
        'admin_actions': 'Admin-Aktionen',
        'reset_password': 'Passwort zurücksetzen',
        'confirm_reset_password': 'Sind Sie sicher, dass Sie das Passwort zurücksetzen möchten?',
        'confirm_delete_user': 'Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?',
        'cannot_delete_self': 'Sie können Ihr eigenes Konto nicht löschen.',
        'user_added': 'Benutzer erfolgreich hinzugefügt.',
        'user_updated': 'Benutzer erfolgreich aktualisiert.',
        'user_deleted': 'Benutzer erfolgreich gelöscht.',
        'user_not_found': 'Benutzer nicht gefunden.',
        'username_exists': 'Benutzername existiert bereits.',
        'email_exists': 'E-Mail existiert bereits.',
        'edit_profile': 'Profil bearbeiten',
        'settings': 'Einstellungen',
        'email_settings': 'E-Mail-Einstellungen',
        'smtp_server': 'SMTP-Server',
        'smtp_port': 'SMTP-Port',
        'use_tls': 'TLS verwenden',
        'email_address': 'E-Mail-Adresse',
        'app_password': 'App-Passwort',
        'sender_address': 'Absenderadresse',
        'settings_saved': 'Einstellungen erfolgreich gespeichert.',
    }
}


def t(key, lang='en'):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)


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
    """Get local logo file or download from web"""
    if os.path.exists(LOCAL_LOGO):
        return LOCAL_LOGO
    # Try to download
    try:
        import urllib.request
        urllib.request.urlretrieve(LOGO_URL, LOCAL_LOGO)
        return LOCAL_LOGO
    except Exception:
        return None


# ==================== LOADING SCREEN ====================

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Jesus Projekt Erfurt")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        # Set icon
        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # Center
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 400) // 2
        self.root.geometry(f"500x400+{x}+{y}")

        # Main container - white card style like web version
        main = tk.Frame(self.root, bg=BG)
        main.pack(expand=True, fill='both')

        # White card
        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)

        # Logo - try to load image, fall back to emoji
        logo_img = get_logo_path()
        if logo_img:
            try:
                img = Image.open(logo_img)
                img.thumbnail((150, 150))
                self.logo_photo = ImageTk.PhotoImage(img)
                tk.Label(card, image=self.logo_photo, bg=WHITE).pack(pady=(30, 10))
            except Exception:
                tk.Label(card, text="🎂", font=("Segoe UI Emoji", 48), bg=WHITE, fg=PRIMARY).pack(pady=(30, 10))
        else:
            tk.Label(card, text="🎂", font=("Segoe UI Emoji", 48), bg=WHITE, fg=PRIMARY).pack(pady=(30, 10))

        # Title
        tk.Label(card, text="Jesus Projekt Erfurt", font=("Segoe UI", 18, "bold"),
                bg=WHITE, fg=PRIMARY).pack()
        tk.Label(card, text="Birthday Monitoring", font=("Segoe UI", 11),
                bg=WHITE, fg=TEXT).pack(pady=(0, 20))

        # Status
        self.status_label = tk.Label(card, text="Loading...", font=("Segoe UI", 10),
                                     bg=WHITE, fg=TEXT)
        self.status_label.pack(pady=(0, 10))

        # Progress bar
        self.progress = ttk.Progressbar(card, length=300, mode='determinate')
        self.progress.pack(pady=(0, 20))

    def update_status(self, text, progress=None):
        self.status_label.config(text=text)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update_idletasks()
        self.root.update()


# ==================== LOGIN WINDOW ====================

class LoginWindow:
    def __init__(self, root, db_path, db_dir, uploads_dir):
        self.root = root
        self.db_path = db_path
        self.db_dir = db_dir
        self.uploads_dir = uploads_dir
        self.engine, self.session = init_db(db_path)
        self.lang = 'en'

        self.root.title("Login - Jesus Projekt Erfurt")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        # Set icon
        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # Center
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 450) // 2
        y = (self.root.winfo_screenheight() - 550) // 2
        self.root.geometry(f"450x550+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        # Main container with padding
        main = tk.Frame(self.root, bg=BG)
        main.pack(expand=True, fill='both', padx=25, pady=50)

        # White card (like web version)
        card = tk.Frame(main, bg=WHITE, bd=1, relief='solid', highlightthickness=0)
        card.pack(fill='both', expand=True)

        inner = tk.Frame(card, bg=WHITE)
        inner.pack(fill='both', expand=True, padx=40, pady=40)

        # Logo
        logo_img = get_logo_path()
        if logo_img:
            try:
                img = Image.open(logo_img)
                img.thumbnail((150, 80))
                self.logo_photo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(inner, image=self.logo_photo, bg=WHITE)
                logo_label.pack(pady=(0, 15))
            except Exception:
                tk.Label(inner, text="🎂", font=("Segoe UI Emoji", 36), bg=WHITE, fg=PRIMARY).pack(pady=(0, 15))
        else:
            tk.Label(inner, text="🎂", font=("Segoe UI Emoji", 36), bg=WHITE, fg=PRIMARY).pack(pady=(0, 15))

        # Title
        self.title_label = tk.Label(inner, text="Jesus Projekt Erfurt",
                                    font=("Segoe UI", 18, "bold"),
                                    bg=WHITE, fg=PRIMARY)
        self.title_label.pack()
        self.subtitle_label = tk.Label(inner, text="Birthday Monitoring",
                                       font=("Segoe UI", 10),
                                       bg=WHITE, fg=TEXT)
        self.subtitle_label.pack(pady=(0, 30))

        # Username field
        self.username_label = tk.Label(inner, text="Username", font=("Segoe UI", 10),
                                      bg=WHITE, fg=TEXT_DARK, anchor='w')
        self.username_label.pack(fill='x')
        username_frame = tk.Frame(inner, bg=WHITE, bd=1, relief='solid', highlightthickness=1,
                                  highlightbackground='#ced4da')
        username_frame.pack(fill='x', pady=(2, 15), ipady=2)
        self.username_icon = tk.Label(username_frame, text="👤", font=("Segoe UI", 11),
                                      bg='#e9ecef', padx=8, pady=4)
        self.username_icon.pack(side='left', fill='y')
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(username_frame, textvariable=self.username_var,
                                       font=("Segoe UI", 11), bd=0, bg=WHITE, relief='flat')
        self.username_entry.pack(side='left', fill='both', expand=True, padx=8, ipady=6)

        # Password field
        self.password_label = tk.Label(inner, text="Password", font=("Segoe UI", 10),
                                      bg=WHITE, fg=TEXT_DARK, anchor='w')
        self.password_label.pack(fill='x')
        password_frame = tk.Frame(inner, bg=WHITE, bd=1, relief='solid', highlightthickness=1,
                                  highlightbackground='#ced4da')
        password_frame.pack(fill='x', pady=(2, 20), ipady=2)
        self.password_icon = tk.Label(password_frame, text="🔒", font=("Segoe UI", 11),
                                      bg='#e9ecef', padx=8, pady=4)
        self.password_icon.pack(side='left', fill='y')
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(password_frame, textvariable=self.password_var,
                                       font=("Segoe UI", 11), bd=0, bg=WHITE,
                                       show='*', relief='flat')
        self.password_entry.pack(side='left', fill='both', expand=True, padx=8, ipady=6)

        # Login button
        self.login_btn = tk.Button(inner, text="🔑  Login", font=("Segoe UI", 11, "bold"),
                                   bg=PRIMARY, fg=WHITE, activebackground=PRIMARY_DARK,
                                   activeforeground=WHITE, relief='flat', cursor='hand2',
                                   bd=0, command=self.do_login)
        self.login_btn.pack(fill='x', pady=(0, 15), ipady=8)

        # Language switcher (same as web version)
        lang_frame = tk.Frame(inner, bg=WHITE)
        lang_frame.pack(pady=(5, 0))
        self.en_btn = tk.Button(lang_frame, text="English", font=("Segoe UI", 9),
                               bg=WHITE, fg=PRIMARY, relief='flat', cursor='hand2',
                               bd=0, activebackground=WHITE,
                               command=lambda: self.set_lang('en'))
        self.en_btn.pack(side='left', padx=5)
        tk.Label(lang_frame, text="|", bg=WHITE, fg=TEXT).pack(side='left')
        self.de_btn = tk.Button(lang_frame, text="Deutsch", font=("Segoe UI", 9),
                               bg=WHITE, fg=TEXT, relief='flat', cursor='hand2',
                               bd=0, activebackground=WHITE,
                               command=lambda: self.set_lang('de'))
        self.de_btn.pack(side='left', padx=5)

        # Status
        self.status_label = tk.Label(inner, text="", font=("Segoe UI", 9),
                                     bg=WHITE, fg=DANGER)
        self.status_label.pack(pady=(10, 0))

        # Bind Enter
        self.root.bind('<Return>', lambda e: self.do_login())
        self.username_entry.focus()

    def set_lang(self, lang):
        self.lang = lang
        self.update_texts()

    def update_texts(self):
        """Update all text elements based on language"""
        self.username_label.config(text=t('username', self.lang))
        self.password_label.config(text=t('password', self.lang))
        self.login_btn.config(text=f"🔑  {t('login', self.lang)}")

        if self.lang == 'en':
            self.en_btn.config(fg=PRIMARY)
            self.de_btn.config(fg=TEXT)
        else:
            self.en_btn.config(fg=TEXT)
            self.de_btn.config(fg=PRIMARY)

    def do_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            self.status_label.config(text="Please enter username and password")
            return

        user = self.session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.is_active:
                self.status_label.config(text=t('account_deactivated', self.lang))
                return

            user.last_login = datetime.utcnow()
            self.session.commit()

            self.root.destroy()
            main_root = tk.Tk()
            MainApp(main_root, self.db_path, self.db_dir, self.uploads_dir, user)
            main_root.mainloop()
        else:
            self.status_label.config(text=t('login_error', self.lang))
            self.password_var.set('')


# ==================== MAIN APP ====================

class MainApp:
    def __init__(self, root, db_path, db_dir, uploads_dir, current_user):
        self.root = root
        self.db_path = db_path
        self.db_dir = db_dir
        self.uploads_dir = uploads_dir
        self.engine, self.session = init_db(db_path)
        self.current_user = current_user
        self.lang = current_user.language or 'en'

        self.root.title("Jesus Projekt Erfurt - Birthday Monitoring")
        self.root.geometry("1200x750")
        self.root.configure(bg=BG)

        # Set icon
        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # Center
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 1200) // 2
        y = (self.root.winfo_screenheight() - 750) // 2
        self.root.geometry(f"1200x750+{x}+{y}")

        self.build_ui()
        self.show_dashboard()

    def build_ui(self):
        # Top navbar (orange like web version)
        navbar = tk.Frame(self.root, bg=PRIMARY, height=56)
        navbar.pack(fill='x')
        navbar.pack_propagate(False)

        # Logo + brand
        brand_frame = tk.Frame(navbar, bg=PRIMARY)
        brand_frame.pack(side='left', padx=15)

        logo_img = get_logo_path()
        if logo_img:
            try:
                img = Image.open(logo_img)
                img.thumbnail((35, 35))
                self.nav_logo = ImageTk.PhotoImage(img)
                tk.Label(brand_frame, image=self.nav_logo, bg=PRIMARY).pack(side='left', padx=(0, 8))
            except Exception:
                tk.Label(brand_frame, text="🎂", font=("Segoe UI Emoji", 18),
                        bg=PRIMARY, fg=WHITE).pack(side='left', padx=(0, 8))

        self.brand_label = tk.Label(brand_frame, text=t('app_name', self.lang),
                                    font=("Segoe UI", 14, "bold"),
                                    bg=PRIMARY, fg=WHITE)
        self.brand_label.pack(side='left', pady=15)

        # Nav items
        nav_items = tk.Frame(navbar, bg=PRIMARY)
        nav_items.pack(side='left', padx=20)

        self.nav_dashboard = tk.Button(nav_items, text=f"🏠 {t('home', self.lang)}",
                                       font=("Segoe UI", 10), bg=PRIMARY, fg=WHITE,
                                       relief='flat', cursor='hand2', bd=0,
                                       activebackground=PRIMARY_DARK,
                                       command=self.show_dashboard)
        self.nav_dashboard.pack(side='left', padx=5, pady=15)

        self.nav_clients = tk.Button(nav_items, text=f"👥 {t('clients', self.lang)}",
                                     font=("Segoe UI", 10), bg=PRIMARY, fg=WHITE,
                                     relief='flat', cursor='hand2', bd=0,
                                     activebackground=PRIMARY_DARK,
                                     command=self.show_clients)
        self.nav_clients.pack(side='left', padx=5, pady=15)

        # Right side - language + user
        right_frame = tk.Frame(navbar, bg=PRIMARY)
        right_frame.pack(side='right', padx=15)

        # Language dropdown
        self.lang_btn = tk.Menubutton(right_frame, text=f"🌐 {t('language', self.lang)}",
                                      font=("Segoe UI", 10), bg=PRIMARY, fg=WHITE,
                                      relief='flat', cursor='hand2', bd=0,
                                      activebackground=PRIMARY_DARK)
        self.lang_menu = tk.Menu(self.lang_btn, tearoff=0)
        self.lang_menu.add_command(label="English", command=lambda: self.switch_lang('en'))
        self.lang_menu.add_command(label="Deutsch", command=lambda: self.switch_lang('de'))
        self.lang_btn.config(menu=self.lang_menu)
        self.lang_btn.pack(side='left', padx=5, pady=15)

        # User dropdown
        role_text = t('admin', self.lang) if self.current_user.has_role('admin') else t('staff', self.lang)
        self.user_btn = tk.Menubutton(right_frame,
                                      text=f"👤 {self.current_user.full_name} ({role_text})",
                                      font=("Segoe UI", 10), bg=PRIMARY, fg=WHITE,
                                      relief='flat', cursor='hand2', bd=0,
                                      activebackground=PRIMARY_DARK)
        self.user_menu = tk.Menu(self.user_btn, tearoff=0)
        self.user_menu.add_command(label=f"✏️ {t('edit_profile', self.lang)}",
                                   command=self.show_profile)
        if self.current_user.has_role('admin'):
            self.user_menu.add_command(label=f"👤 {t('users', self.lang)}",
                                       command=self.show_users)
            self.user_menu.add_command(label=f"⚙️ {t('settings', self.lang)}",
                                       command=self.show_settings)
        self.user_menu.add_separator()
        self.user_menu.add_command(label=f"🚪 {t('logout', self.lang)}",
                                   command=self.logout)
        self.user_btn.config(menu=self.user_menu)
        self.user_btn.pack(side='left', padx=5, pady=15)

        # Content area
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(fill='both', expand=True)

    def switch_lang(self, lang):
        self.lang = lang
        self.current_user.language = lang
        self.session.commit()
        # Rebuild UI with new language
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_ui()
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ==================== DASHBOARD ====================

    def show_dashboard(self):
        self.clear_content()

        # Header
        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=(20, 10))
        tk.Label(header, text=f"📅 {t('dashboard', self.lang)}",
                font=("Segoe UI", 22, "bold"), bg=BG, fg=DARK).pack(side='left')

        # Stats cards
        stats_frame = tk.Frame(self.content, bg=BG)
        stats_frame.pack(fill='x', padx=20, pady=10)

        total_clients = self.session.query(Client).count()

        # Total clients card (orange like web)
        self.create_stat_card(stats_frame, t('total_clients', self.lang), str(total_clients),
                             PRIMARY, "👥").pack(side='left', padx=5, fill='x', expand=True)

        # Today's birthdays
        today_str = date.today().strftime('%m-%d')
        today_birthdays = self.session.query(Client).filter(
            Client.birthday.like(f'%-{today_str}')
        ).count()
        self.create_stat_card(stats_frame, "Today's Birthdays" if self.lang == 'en' else "Heutige Geburtstage",
                             str(today_birthdays), SECONDARY, "🎂").pack(side='left', padx=5, fill='x', expand=True)

        # Birthday celebrants card
        main_card = tk.Frame(self.content, bg=WHITE, bd=0, highlightthickness=1,
                            highlightbackground='#e0e0e0')
        main_card.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Card header
        card_header = tk.Frame(main_card, bg=WHITE)
        card_header.pack(fill='x', padx=20, pady=(15, 10))

        tk.Label(card_header, text=f"📆 {t('birthday_celebrants', self.lang)}",
                font=("Segoe UI", 14, "bold"), bg=WHITE, fg=DARK).pack(side='left')

        # Send Greetings button (right side)
        self.send_btn = tk.Button(card_header, text=f"📧 {t('send_greetings', self.lang)}",
                                  font=("Segoe UI", 10, "bold"),
                                  bg=SUCCESS, fg=WHITE, relief='flat', cursor='hand2',
                                  bd=0, command=self.open_send_greetings)
        self.send_btn.pack(side='right')

        # Month selector
        select_frame = tk.Frame(main_card, bg=WHITE)
        select_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(select_frame, text=t('select_month', self.lang) + ":",
                font=("Segoe UI", 11), bg=WHITE).pack(side='left', padx=(0, 10))

        months = [t('all_months', self.lang),
                 t('january', self.lang), t('february', self.lang), t('march', self.lang),
                 t('april', self.lang), t('may', self.lang), t('june', self.lang),
                 t('july', self.lang), t('august', self.lang), t('september', self.lang),
                 t('october', self.lang), t('november', self.lang), t('december', self.lang)]

        self.month_var = tk.StringVar(value=t('all_months', self.lang))
        self.month_combo = ttk.Combobox(select_frame, textvariable=self.month_var,
                                        values=months, state='readonly', width=20,
                                        font=("Segoe UI", 11))
        self.month_combo.pack(side='left', padx=(0, 10))
        self.month_combo.bind('<<ComboboxSelected>>', lambda e: self.load_birthday_list())

        # Table
        table_frame = tk.Frame(main_card, bg=WHITE)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = (t('first_name', self.lang), t('last_name', self.lang),
                  t('birthday', self.lang), t('age', self.lang),
                  t('phone', self.lang), t('email', self.lang),
                  t('privacy_signed', self.lang), t('photo_permission', self.lang))

        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        widths = [120, 120, 100, 60, 120, 180, 80, 80]
        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor='center')

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.load_birthday_list()

    def create_stat_card(self, parent, title, value, color, icon):
        card = tk.Frame(parent, bg=color, bd=0)
        content = tk.Frame(card, bg=color)
        content.pack(fill='both', expand=True, padx=20, pady=15)

        top = tk.Frame(content, bg=color)
        top.pack(fill='x')
        tk.Label(top, text=title, font=("Segoe UI", 11), bg=color, fg=WHITE).pack(side='left')
        tk.Label(top, text=icon, font=("Segoe UI Emoji", 20), bg=color, fg=WHITE).pack(side='right')

        tk.Label(content, text=value, font=("Segoe UI", 28, "bold"), bg=color, fg=WHITE).pack(anchor='w', pady=(8, 0))
        return card

    def load_birthday_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected = self.month_var.get()
        query = self.session.query(Client)

        if selected != t('all_months', self.lang):
            months = [t('january', self.lang), t('february', self.lang), t('march', self.lang),
                     t('april', self.lang), t('may', self.lang), t('june', self.lang),
                     t('july', self.lang), t('august', self.lang), t('september', self.lang),
                     t('october', self.lang), t('november', self.lang), t('december', self.lang)]
            month_num = months.index(selected) + 1
            query = query.filter(Client.birthday.like(f'%-{month_num:02d}-%'))

        clients = query.order_by(Client.birthday).all()
        self.current_month_clients = clients

        # Show/hide send button
        has_email = any(c.email for c in clients)
        if hasattr(self, 'send_btn'):
            if has_email:
                self.send_btn.pack(side='right')
            else:
                self.send_btn.pack_forget()

        for c in clients:
            self.tree.insert('', 'end', iid=c.id, values=(
                c.first_name, c.last_name,
                c.birthday.strftime('%d.%m.%Y'),
                c.age,
                c.phone or '-',
                c.email or '-',
                '✓' if c.privacy_signed else '✗',
                '✓' if c.photo_permission else '✗'
            ))

        if not clients:
            # Show empty state
            empty = tk.Label(self.tree.master, text=t('no_celebrants', self.lang),
                           font=("Segoe UI", 12), bg=WHITE, fg=TEXT)
            empty.place(relx=0.5, rely=0.5, anchor='center')

    def open_send_greetings(self):
        clients = getattr(self, 'current_month_clients', [])
        clients_with_email = [c for c in clients if c.email]
        if not clients_with_email:
            messagebox.showwarning("No Recipients", t('no_email_clients', self.lang))
            return
        GreetingDialog(self.root, self.session, clients_with_email, self)

    # ==================== CLIENTS ====================

    def show_clients(self):
        self.clear_content()

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=(20, 10))
        tk.Label(header, text=f"👥 {t('clients', self.lang)}",
                font=("Segoe UI", 22, "bold"), bg=BG, fg=DARK).pack(side='left')

        tk.Button(header, text=f"➕ {t('add_client', self.lang)}",
                 font=("Segoe UI", 10, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 bd=0, command=self.open_add_client).pack(side='right')

        # Table
        table_card = tk.Frame(self.content, bg=WHITE, bd=0, highlightthickness=1,
                              highlightbackground='#e0e0e0')
        table_card.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        table_frame = tk.Frame(table_card, bg=WHITE)
        table_frame.pack(fill='both', expand=True, padx=15, pady=15)

        columns = (t('first_name', self.lang), t('last_name', self.lang),
                  t('birthday', self.lang), t('age', self.lang),
                  t('phone', self.lang), t('email', self.lang), t('actions', self.lang))

        self.client_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=18)
        widths = [120, 120, 100, 60, 120, 180, 100]
        for col, w in zip(columns, widths):
            self.client_tree.heading(col, text=col)
            self.client_tree.column(col, width=w, anchor='center')

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=scrollbar.set)
        self.client_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.client_tree.bind('<Double-1>', self.edit_client_event)

        self.load_clients()

    def load_clients(self):
        if hasattr(self, 'client_tree'):
            for item in self.client_tree.get_children():
                self.client_tree.delete(item)
            clients = self.session.query(Client).order_by(Client.last_name).all()
            for c in clients:
                self.client_tree.insert('', 'end', iid=c.id, values=(
                    c.first_name, c.last_name,
                    c.birthday.strftime('%d.%m.%Y'),
                    c.age,
                    c.phone or '-',
                    c.email or '-',
                    "✏️ 🗑️" if self.current_user.has_role('admin') else "✏️"
                ))

    def edit_client_event(self, event):
        item = self.client_tree.selection()
        if item:
            self.open_edit_client(int(item[0]))

    def open_add_client(self):
        ClientDialog(self.root, self.session, self.uploads_dir, self.load_clients, self.lang)

    def open_edit_client(self, client_id):
        client = self.session.query(Client).get(client_id)
        if client:
            ClientDialog(self.root, self.session, self.uploads_dir, self.load_clients, self.lang, client, self.current_user)

    # ==================== USERS ====================

    def show_users(self):
        if not self.current_user.has_role('admin'):
            return
        self.clear_content()

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=(20, 10))
        tk.Label(header, text=f"👤 {t('user_management', self.lang)}",
                font=("Segoe UI", 22, "bold"), bg=BG, fg=DARK).pack(side='left')

        tk.Button(header, text=f"➕ {t('add_user', self.lang)}",
                 font=("Segoe UI", 10, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 bd=0, command=self.open_add_user).pack(side='right')

        table_card = tk.Frame(self.content, bg=WHITE, bd=0, highlightthickness=1,
                              highlightbackground='#e0e0e0')
        table_card.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        table_frame = tk.Frame(table_card, bg=WHITE)
        table_frame.pack(fill='both', expand=True, padx=15, pady=15)

        columns = (t('username', self.lang), t('email', self.lang),
                  t('first_name', self.lang), t('last_name', self.lang),
                  t('role', self.lang), t('status', self.lang), t('last_login', self.lang), t('actions', self.lang))

        self.user_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=18)
        widths = [100, 150, 100, 100, 80, 80, 130, 80]
        for col, w in zip(columns, widths):
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=w, anchor='center')

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        self.user_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.user_tree.bind('<Double-1>', self.edit_user_event)
        self.load_users()

    def load_users(self):
        if hasattr(self, 'user_tree'):
            for item in self.user_tree.get_children():
                self.user_tree.delete(item)
            users = self.session.query(User).order_by(User.username).all()
            for u in users:
                self.user_tree.insert('', 'end', iid=u.id, values=(
                    u.username, u.email, u.first_name or '-', u.last_name or '-',
                    t(u.role, self.lang),
                    t('active', self.lang) if u.is_active else t('inactive', self.lang),
                    u.last_login.strftime('%d.%m.%Y %H:%M') if u.last_login else '-',
                    "✏️ 🗑️" if u.id != self.current_user.id else "✏️"
                ))

    def edit_user_event(self, event):
        item = self.user_tree.selection()
        if item:
            self.open_edit_user(int(item[0]))

    def open_add_user(self):
        UserDialog(self.root, self.session, self.uploads_dir, self.load_users, self.lang, is_admin=True)

    def open_edit_user(self, user_id):
        user = self.session.query(User).get(user_id)
        if user:
            UserDialog(self.root, self.session, self.uploads_dir, self.load_users, self.lang, user, self.current_user, is_admin=True)

    # ==================== SETTINGS ====================

    def show_settings(self):
        if not self.current_user.has_role('admin'):
            return
        self.clear_content()

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=(20, 10))
        tk.Label(header, text=f"⚙️ {t('email_settings', self.lang)}",
                font=("Segoe UI", 22, "bold"), bg=BG, fg=DARK).pack(side='left')

        # Form card
        form_card = tk.Frame(self.content, bg=WHITE, bd=0, highlightthickness=1,
                            highlightbackground='#e0e0e0')
        form_card.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        form = tk.Frame(form_card, bg=WHITE)
        form.pack(fill='both', expand=True, padx=40, pady=30)

        def get_setting(key, default=''):
            s = self.session.query(Settings).filter_by(key=key).first()
            return s.value if s else default

        self.smtp_server_var = tk.StringVar(value=get_setting('mail_server', 'smtp.gmail.com'))
        self.smtp_port_var = tk.StringVar(value=get_setting('mail_port', '587'))
        self.smtp_username_var = tk.StringVar(value=get_setting('mail_username', ''))
        self.smtp_password_var = tk.StringVar(value=get_setting('mail_password', ''))
        self.smtp_sender_var = tk.StringVar(value=get_setting('mail_default_sender', ''))
        self.smtp_tls_var = tk.BooleanVar(value=get_setting('mail_use_tls', 'true') == 'true')

        fields = [
            (t('smtp_server', self.lang), self.smtp_server_var, False),
            (t('smtp_port', self.lang), self.smtp_port_var, False),
            (t('email_address', self.lang), self.smtp_username_var, False),
            (t('app_password', self.lang), self.smtp_password_var, True),
            (t('sender_address', self.lang), self.smtp_sender_var, False),
        ]

        row = 0
        for label, var, is_password in fields:
            tk.Label(form, text=label, font=("Segoe UI", 11), bg=WHITE, anchor='w').grid(
                row=row, column=0, sticky='w', padx=5, pady=10)
            entry = tk.Entry(form, textvariable=var, font=("Segoe UI", 11), width=40, relief='solid', bd=1)
            if is_password:
                entry.config(show='*')
            entry.grid(row=row, column=1, sticky='ew', padx=5, pady=10)
            row += 1

        tk.Label(form, text=t('use_tls', self.lang), font=("Segoe UI", 11), bg=WHITE).grid(
            row=row, column=0, sticky='w', padx=5, pady=10)
        tk.Checkbutton(form, variable=self.smtp_tls_var, bg=WHITE).grid(
            row=row, column=1, sticky='w', padx=5, pady=10)
        row += 1

        form.columnconfigure(1, weight=1)

        tk.Button(form, text=f"💾 {t('save', self.lang)}",
                 font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.save_settings).grid(row=row, column=0, columnspan=2, pady=20, ipadx=20, ipady=8)

    def save_settings(self):
        def set_setting(key, value):
            s = self.session.query(Settings).filter_by(key=key).first()
            if s:
                s.value = str(value)
                s.updated_at = datetime.utcnow()
            else:
                s = Settings(key=key, value=str(value))
                self.session.add(s)

        set_setting('mail_server', self.smtp_server_var.get())
        set_setting('mail_port', self.smtp_port_var.get())
        set_setting('mail_username', self.smtp_username_var.get())
        set_setting('mail_password', self.smtp_password_var.get())
        set_setting('mail_default_sender', self.smtp_sender_var.get())
        set_setting('mail_use_tls', 'true' if self.smtp_tls_var.get() else 'false')

        self.session.commit()
        messagebox.showinfo(t('app_name', self.lang), t('settings_saved', self.lang))

    # ==================== PROFILE ====================

    def show_profile(self):
        ProfileDialog(self.root, self.session, self.uploads_dir, self.lang, self)

    # ==================== LOGOUT ====================

    def logout(self):
        self.root.destroy()
        login_root = tk.Tk()
        LoginWindow(login_root, self.db_path, self.db_dir, self.uploads_dir)
        login_root.mainloop()


# ==================== DIALOGS ====================

class ClientDialog:
    def __init__(self, parent, session, uploads_dir, refresh_callback, lang, client=None, current_user=None):
        self.session = session
        self.uploads_dir = uploads_dir
        self.refresh_callback = refresh_callback
        self.client = client
        self.current_user = current_user
        self.lang = lang

        self.top = tk.Toplevel(parent)
        self.top.title(t('add_client' if client is None else 'edit_client', lang) +
                      " - Jesus Projekt Erfurt")
        self.top.geometry("550x700")
        self.top.configure(bg=BG)
        self.top.transient(parent)
        self.top.grab_set()

        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.top.iconbitmap(icon_path)
        except Exception:
            pass

        self.top.update_idletasks()
        x = (parent.winfo_screenwidth() - 550) // 2
        y = (parent.winfo_screenheight() - 700) // 2
        self.top.geometry(f"550x700+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        # Card
        main = tk.Frame(self.top, bg=BG)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=1, highlightbackground='#e0e0e0')
        card.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(card, bg=WHITE)
        header.pack(fill='x', padx=25, pady=(20, 0))
        mode = 'add' if self.client is None else 'edit'
        icon = '➕' if mode == 'add' else '✏️'
        tk.Label(header, text=f"{icon} {t('add_client' if mode == 'add' else 'edit_client', self.lang)}",
                font=("Segoe UI", 16, "bold"), bg=WHITE, fg=PRIMARY).pack(anchor='w')

        # Form
        form = tk.Frame(card, bg=WHITE)
        form.pack(fill='both', expand=True, padx=25, pady=20)

        self.first_name_var = tk.StringVar(value=self.client.first_name if self.client else '')
        self.last_name_var = tk.StringVar(value=self.client.last_name if self.client else '')
        self.address_var = tk.StringVar(value=self.client.address if self.client else '')
        self.phone_var = tk.StringVar(value=self.client.phone if self.client else '')
        self.email_var = tk.StringVar(value=self.client.email if self.client else '')
        self.privacy_var = tk.BooleanVar(value=self.client.privacy_signed if self.client else False)
        self.photo_var = tk.BooleanVar(value=self.client.photo_permission if self.client else False)

        fields = [
            (t('first_name', self.lang) + " *", self.first_name_var),
            (t('last_name', self.lang) + " *", self.last_name_var),
            (t('address', self.lang), self.address_var),
            (t('phone', self.lang), self.phone_var),
            (t('email', self.lang), self.email_var),
        ]

        for label, var in fields:
            tk.Label(form, text=label, font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(8, 0))
            entry = tk.Entry(form, textvariable=var, font=("Segoe UI", 11), relief='solid', bd=1)
            entry.pack(fill='x', pady=(2, 5), ipady=4)

        tk.Label(form, text=t('birthday', self.lang) + " * (YYYY-MM-DD)",
                font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(8, 0))
        self.birthday_entry = tk.Entry(form, font=("Segoe UI", 11), relief='solid', bd=1)
        if self.client:
            self.birthday_entry.insert(0, self.client.birthday.strftime('%Y-%m-%d'))
        else:
            self.birthday_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.birthday_entry.pack(fill='x', pady=(2, 5), ipady=4)

        # Switches
        switch_frame = tk.Frame(form, bg=WHITE)
        switch_frame.pack(fill='x', pady=10)
        tk.Checkbutton(switch_frame, text=t('privacy_signed', self.lang),
                      variable=self.privacy_var, bg=WHITE,
                      font=("Segoe UI", 10)).pack(anchor='w', pady=2)
        tk.Checkbutton(switch_frame, text=t('photo_permission', self.lang),
                      variable=self.photo_var, bg=WHITE,
                      font=("Segoe UI", 10)).pack(anchor='w', pady=2)

        # Buttons
        btn_frame = tk.Frame(card, bg=WHITE)
        btn_frame.pack(fill='x', padx=25, pady=(0, 20))

        tk.Button(btn_frame, text=f"💾 {t('save', self.lang)}",
                 font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.save).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)

        # Delete button (admin only, edit mode)
        if self.client and self.current_user and self.current_user.has_role('admin'):
            tk.Button(btn_frame, text=f"🗑️ {t('delete', self.lang)}",
                     font=("Segoe UI", 11, "bold"),
                     bg=DANGER, fg=WHITE, relief='flat', cursor='hand2', bd=0,
                     command=self.delete_client).pack(side='left', padx=5, ipady=8)

        tk.Button(btn_frame, text=t('cancel', self.lang),
                 font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def delete_client(self):
        if not self.client:
            return

        # Admin password confirmation
        password = tk.simpledialog.askstring(
            t('confirm_delete', self.lang),
            t('admin_password', self.lang) + ":",
            show='*',
            parent=self.top
        )

        if not password:
            return

        if not self.current_user.check_password(password):
            messagebox.showerror(t('app_name', self.lang), t('incorrect_password', self.lang))
            return

        self.session.delete(self.client)
        self.session.commit()
        messagebox.showinfo(t('app_name', self.lang), t('client_deleted', self.lang))
        self.refresh_callback()
        self.top.destroy()

    def save(self):
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        birthday_str = self.birthday_entry.get().strip()

        if not first_name or not last_name or not birthday_str:
            messagebox.showerror(t('app_name', self.lang), t('required_field', self.lang))
            return

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror(t('app_name', self.lang), "Invalid date format. Use YYYY-MM-DD.")
            return

        if self.client:
            self.client.first_name = first_name
            self.client.last_name = last_name
            self.client.address = self.address_var.get().strip()
            self.client.phone = self.phone_var.get().strip()
            self.client.email = self.email_var.get().strip()
            self.client.birthday = birthday
            self.client.privacy_signed = self.privacy_var.get()
            self.client.photo_permission = self.photo_var.get()
            message = t('client_updated', self.lang)
        else:
            client = Client(
                first_name=first_name,
                last_name=last_name,
                address=self.address_var.get().strip(),
                phone=self.phone_var.get().strip(),
                email=self.email_var.get().strip(),
                birthday=birthday,
                privacy_signed=self.privacy_var.get(),
                photo_permission=self.photo_var.get()
            )
            self.session.add(client)
            message = t('client_added', self.lang)

        self.session.commit()
        messagebox.showinfo(t('app_name', self.lang), message)
        self.refresh_callback()
        self.top.destroy()


class UserDialog:
    def __init__(self, parent, session, uploads_dir, refresh_callback, lang, user=None, current_user=None, is_admin=False):
        self.session = session
        self.uploads_dir = uploads_dir
        self.refresh_callback = refresh_callback
        self.user = user
        self.current_user = current_user
        self.is_admin = is_admin
        self.lang = lang
        self.profile_picture_path = None

        self.top = tk.Toplevel(parent)
        self.top.title(t('add_user' if user is None else 'edit_user', lang) +
                      " - Jesus Projekt Erfurt")
        self.top.geometry("550x750")
        self.top.configure(bg=BG)
        self.top.transient(parent)
        self.top.grab_set()

        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.top.iconbitmap(icon_path)
        except Exception:
            pass

        self.top.update_idletasks()
        x = (parent.winfo_screenwidth() - 550) // 2
        y = (parent.winfo_screenheight() - 750) // 2
        self.top.geometry(f"550x750+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        main = tk.Frame(self.top, bg=BG)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=1, highlightbackground='#e0e0e0')
        card.pack(fill='both', expand=True)

        header = tk.Frame(card, bg=WHITE)
        header.pack(fill='x', padx=25, pady=(20, 0))
        mode = 'add' if self.user is None else 'edit'
        icon = '➕' if mode == 'add' else '✏️'
        tk.Label(header, text=f"{icon} {t('add_user' if mode == 'add' else 'edit_user', self.lang)}",
                font=("Segoe UI", 16, "bold"), bg=WHITE, fg=PRIMARY).pack(anchor='w')

        form = tk.Frame(card, bg=WHITE)
        form.pack(fill='both', expand=True, padx=25, pady=20)

        self.username_var = tk.StringVar(value=self.user.username if self.user else '')
        self.email_var = tk.StringVar(value=self.user.email if self.user else '')
        self.first_name_var = tk.StringVar(value=self.user.first_name if self.user else '')
        self.last_name_var = tk.StringVar(value=self.user.last_name if self.user else '')
        self.role_var = tk.StringVar(value=self.user.role if self.user else 'staff')
        self.active_var = tk.BooleanVar(value=self.user.is_active if self.user else True)

        fields = [
            (t('username', self.lang) + " *", self.username_var),
            (t('email', self.lang) + " *", self.email_var),
            (t('first_name', self.lang), self.first_name_var),
            (t('last_name', self.lang), self.last_name_var),
        ]

        for label, var in fields:
            tk.Label(form, text=label, font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(8, 0))
            tk.Entry(form, textvariable=var, font=("Segoe UI", 11), relief='solid', bd=1).pack(fill='x', pady=(2, 5), ipady=4)

        pw_label = t('password', self.lang) if not self.user else t('new_password', self.lang)
        if not self.user:
            pw_label += " *"
        tk.Label(form, text=pw_label, font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(8, 0))
        self.password_entry = tk.Entry(form, font=("Segoe UI", 11), show='*', relief='solid', bd=1)
        self.password_entry.pack(fill='x', pady=(2, 2), ipady=4)
        if self.user:
            tk.Label(form, text=t('leave_blank_no_change', self.lang),
                    font=("Segoe UI", 8), bg=WHITE, fg=TEXT).pack(anchor='w', pady=(0, 5))

        if self.is_admin:
            tk.Label(form, text=t('role', self.lang), font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(8, 0))
            role_combo = ttk.Combobox(form, textvariable=self.role_var,
                                      values=[t('staff', self.lang), t('admin', self.lang)],
                                      state='readonly', font=("Segoe UI", 11))
            # Map translated values to actual roles
            role_to_display = {'staff': t('staff', self.lang), 'admin': t('admin', self.lang)}
            display_to_role = {v: k for k, v in role_to_display.items()}
            if self.user:
                role_combo.set(role_to_display.get(self.user.role, t('staff', self.lang)))
            else:
                role_combo.set(t('staff', self.lang))
            role_combo.pack(fill='x', pady=(2, 5), ipady=4)
            self.role_combo = role_combo
            self.display_to_role = display_to_role

            tk.Checkbutton(form, text=t('active', self.lang),
                          variable=self.active_var, bg=WHITE,
                          font=("Segoe UI", 10)).pack(anchor='w', pady=5)

        # Profile picture
        pic_frame = tk.Frame(form, bg=WHITE)
        pic_frame.pack(fill='x', pady=15)
        self.pic_label = tk.Label(pic_frame, text="📷", font=("Segoe UI Emoji", 30),
                                  bg='#e9ecef', width=6, height=3)
        self.pic_label.pack(side='left', padx=(0, 15))
        tk.Button(pic_frame, text=f"📁 {t('profile_picture', self.lang)}",
                 font=("Segoe UI", 10),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.upload_photo).pack(side='left', pady=20, ipadx=10, ipady=5)

        if self.user and self.user.profile_picture:
            self.load_user_picture()

        # Buttons
        btn_frame = tk.Frame(card, bg=WHITE)
        btn_frame.pack(fill='x', padx=25, pady=(0, 20))

        tk.Button(btn_frame, text=f"💾 {t('save', self.lang)}",
                 font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.save).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)

        if self.user and self.current_user and self.user.id != self.current_user.id:
            tk.Button(btn_frame, text=f"🗑️ {t('delete', self.lang)}",
                     font=("Segoe UI", 11, "bold"),
                     bg=DANGER, fg=WHITE, relief='flat', cursor='hand2', bd=0,
                     command=self.delete_user).pack(side='left', padx=5, ipady=8)

        tk.Button(btn_frame, text=t('cancel', self.lang),
                 font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def upload_photo(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if filename:
            if os.path.getsize(filename) > 5 * 1024 * 1024:
                messagebox.showerror(t('app_name', self.lang), "File too large (max 5MB)")
                return
            self.profile_picture_path = filename
            self.load_picture_preview(filename)

    def load_picture_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(img)
            self.pic_label.config(image=photo, text='', width=100, height=100)
            self.pic_label.image = photo
        except Exception as e:
            print(f"Error: {e}")

    def load_user_picture(self):
        if self.user and self.user.profile_picture:
            path = os.path.join(self.uploads_dir, self.user.profile_picture)
            if os.path.exists(path):
                self.load_picture_preview(path)

    def save(self):
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_entry.get()

        if not username or not email:
            messagebox.showerror(t('app_name', self.lang), t('required_field', self.lang))
            return

        if not self.user and not password:
            messagebox.showerror(t('app_name', self.lang), "Password required for new users")
            return

        if not self.user:
            if self.session.query(User).filter_by(username=username).first():
                messagebox.showerror(t('app_name', self.lang), t('username_exists', self.lang))
                return
            if self.session.query(User).filter_by(email=email).first():
                messagebox.showerror(t('app_name', self.lang), t('email_exists', self.lang))
                return

        # Get role
        role = self.role_var.get()
        if self.is_admin and hasattr(self, 'display_to_role'):
            role = self.display_to_role.get(role, 'staff')

        if self.user:
            self.user.username = username
            self.user.email = email
            self.user.first_name = self.first_name_var.get().strip()
            self.user.last_name = self.last_name_var.get().strip()
            if self.is_admin:
                self.user.role = role
                self.user.is_active = self.active_var.get()
            if password:
                self.user.set_password(password)
        else:
            user = User(
                username=username,
                email=email,
                first_name=self.first_name_var.get().strip(),
                last_name=self.last_name_var.get().strip(),
                role=role if self.is_admin else 'staff',
                is_active=self.active_var.get() if self.is_admin else True,
            )
            user.set_password(password)
            self.session.add(user)
            self.session.commit()
            self.user = user

        # Save profile picture
        if self.profile_picture_path:
            ext = os.path.splitext(self.profile_picture_path)[1]
            filename = f"user_{self.user.id}_{uuid.uuid4().hex[:8]}{ext}"
            dest = os.path.join(self.uploads_dir, filename)
            os.makedirs(self.uploads_dir, exist_ok=True)
            shutil.copy(self.profile_picture_path, dest)
            self.user.profile_picture = filename

        self.session.commit()
        messagebox.showinfo(t('app_name', self.lang),
                          t('user_added' if not hasattr(self, '_was_new') else 'user_updated', self.lang))
        self.refresh_callback()
        self.top.destroy()

    def delete_user(self):
        if not self.user:
            return
        if not messagebox.askyesno(t('confirm_delete', self.lang),
                                   t('confirm_delete_user', self.lang)):
            return

        # Admin password
        password = tk.simpledialog.askstring(
            t('confirm_delete', self.lang),
            t('admin_password', self.lang) + ":",
            show='*', parent=self.top
        )
        if not password:
            return

        if not self.current_user.check_password(password):
            messagebox.showerror(t('app_name', self.lang), t('incorrect_password', self.lang))
            return

        self.session.delete(self.user)
        self.session.commit()
        messagebox.showinfo(t('app_name', self.lang), t('user_deleted', self.lang))
        self.refresh_callback()
        self.top.destroy()


class ProfileDialog:
    def __init__(self, parent, session, uploads_dir, lang, main_app):
        self.session = session
        self.uploads_dir = uploads_dir
        self.user = main_app.current_user
        self.lang = lang
        self.main_app = main_app
        self.profile_picture_path = None

        self.top = tk.Toplevel(parent)
        self.top.title(t('edit_profile', lang) + " - Jesus Projekt Erfurt")
        self.top.geometry("550x650")
        self.top.configure(bg=BG)
        self.top.transient(parent)
        self.top.grab_set()

        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.top.iconbitmap(icon_path)
        except Exception:
            pass

        self.build_ui()

    def build_ui(self):
        main = tk.Frame(self.top, bg=BG)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=1, highlightbackground='#e0e0e0')
        card.pack(fill='both', expand=True)

        header = tk.Frame(card, bg=WHITE)
        header.pack(fill='x', padx=25, pady=(20, 0))
        tk.Label(header, text=f"👤 {t('edit_profile', self.lang)}",
                font=("Segoe UI", 16, "bold"), bg=WHITE, fg=PRIMARY).pack(anchor='w')

        form = tk.Frame(card, bg=WHITE)
        form.pack(fill='both', expand=True, padx=25, pady=20)

        self.username_var = tk.StringVar(value=self.user.username)
        self.email_var = tk.StringVar(value=self.user.email)
        self.first_name_var = tk.StringVar(value=self.user.first_name or '')
        self.last_name_var = tk.StringVar(value=self.user.last_name or '')

        fields = [
            (t('username', self.lang) + " *", self.username_var),
            (t('email', self.lang) + " *", self.email_var),
            (t('first_name', self.lang), self.first_name_var),
            (t('last_name', self.lang), self.last_name_var),
        ]

        for label, var in fields:
            tk.Label(form, text=label, font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(8, 0))
            tk.Entry(form, textvariable=var, font=("Segoe UI", 11), relief='solid', bd=1).pack(fill='x', pady=(2, 5), ipady=4)

        tk.Label(form, text=t('new_password', self.lang), font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(8, 0))
        self.password_entry = tk.Entry(form, font=("Segoe UI", 11), show='*', relief='solid', bd=1)
        self.password_entry.pack(fill='x', pady=(2, 2), ipady=4)
        tk.Label(form, text=t('leave_blank_no_change', self.lang),
                font=("Segoe UI", 8), bg=WHITE, fg=TEXT).pack(anchor='w', pady=(0, 5))

        # Profile picture
        pic_frame = tk.Frame(form, bg=WHITE)
        pic_frame.pack(fill='x', pady=15)
        self.pic_label = tk.Label(pic_frame, text="👤", font=("Segoe UI Emoji", 30),
                                  bg='#e9ecef', width=6, height=3)
        self.pic_label.pack(side='left', padx=(0, 15))

        if self.user.profile_picture:
            self.load_user_picture()
            tk.Button(pic_frame, text=f"🔄 Change {t('profile_picture', self.lang)}",
                     font=("Segoe UI", 10),
                     bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2', bd=0,
                     command=self.upload_photo).pack(side='left', pady=20, ipadx=10, ipady=5)
        else:
            tk.Button(pic_frame, text=f"📁 Upload {t('profile_picture', self.lang)}",
                     font=("Segoe UI", 10),
                     bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2', bd=0,
                     command=self.upload_photo).pack(side='left', pady=20, ipadx=10, ipady=5)

        # Buttons
        btn_frame = tk.Frame(card, bg=WHITE)
        btn_frame.pack(fill='x', padx=25, pady=(0, 20))

        tk.Button(btn_frame, text=f"💾 {t('save', self.lang)}",
                 font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.save).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)

        tk.Button(btn_frame, text=t('cancel', self.lang),
                 font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def upload_photo(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if filename:
            if os.path.getsize(filename) > 5 * 1024 * 1024:
                messagebox.showerror(t('app_name', self.lang), "File too large (max 5MB)")
                return
            self.profile_picture_path = filename
            try:
                img = Image.open(filename)
                img.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(img)
                self.pic_label.config(image=photo, text='', width=100, height=100)
                self.pic_label.image = photo
            except Exception as e:
                print(f"Error: {e}")

    def load_user_picture(self):
        path = os.path.join(self.uploads_dir, self.user.profile_picture)
        if os.path.exists(path):
            try:
                img = Image.open(path)
                img.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(img)
                self.pic_label.config(image=photo, text='', width=100, height=100)
                self.pic_label.image = photo
            except Exception:
                pass

    def save(self):
        self.user.username = self.username_var.get().strip()
        self.user.email = self.email_var.get().strip()
        self.user.first_name = self.first_name_var.get().strip()
        self.user.last_name = self.last_name_var.get().strip()

        password = self.password_entry.get()
        if password:
            self.user.set_password(password)

        if self.profile_picture_path:
            ext = os.path.splitext(self.profile_picture_path)[1]
            filename = f"user_{self.user.id}_{uuid.uuid4().hex[:8]}{ext}"
            dest = os.path.join(self.uploads_dir, filename)
            os.makedirs(self.uploads_dir, exist_ok=True)
            shutil.copy(self.profile_picture_path, dest)
            self.user.profile_picture = filename

        self.session.commit()
        messagebox.showinfo(t('app_name', self.lang), t('user_updated', self.lang))
        self.top.destroy()


class GreetingDialog:
    def __init__(self, parent, session, clients, main_app):
        self.session = session
        self.clients = clients
        self.main_app = main_app
        self.lang = main_app.lang

        self.top = tk.Toplevel(parent)
        self.top.title(t('send_greetings', self.lang) + " - Jesus Projekt Erfurt")
        self.top.geometry("650x550")
        self.top.configure(bg=BG)
        self.top.transient(parent)
        self.top.grab_set()

        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.top.iconbitmap(icon_path)
        except Exception:
            pass

        self.build_ui()

    def build_ui(self):
        main = tk.Frame(self.top, bg=BG)
        main.pack(fill='both', expand=True, padx=20, pady=20)

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=1, highlightbackground='#e0e0e0')
        card.pack(fill='both', expand=True)

        header = tk.Frame(card, bg=WHITE)
        header.pack(fill='x', padx=25, pady=(20, 10))
        tk.Label(header, text=f"📧 {t('send_greetings', self.lang)}",
                font=("Segoe UI", 16, "bold"), bg=WHITE, fg=PRIMARY).pack(anchor='w')

        # Info
        tk.Label(card, text=f"ℹ️ {t('placeholders_info', self.lang) if 'placeholders_info' in TRANSLATIONS.get(self.lang, {}) else 'Use {name} for client name'}",
                font=("Segoe UI", 9), bg='#fff3cd', fg='#856404', anchor='w').pack(fill='x', padx=25, pady=(0, 10))

        form = tk.Frame(card, bg=WHITE)
        form.pack(fill='both', expand=True, padx=25)

        tk.Label(form, text=t('subject', self.lang), font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x')
        self.subject_entry = tk.Entry(form, font=("Segoe UI", 11), relief='solid', bd=1)
        self.subject_entry.insert(0, t('greeting_subject', self.lang).replace('{name}', '[Name]'))
        self.subject_entry.pack(fill='x', pady=(2, 10), ipady=4)

        tk.Label(form, text=t('message', self.lang), font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x')
        self.message_text = tk.Text(form, font=("Segoe UI", 10), height=10, wrap='word', relief='solid', bd=1)
        self.message_text.insert('1.0', t('greeting_message', self.lang).replace('{name}', '[Name]'))
        self.message_text.pack(fill='both', expand=True, pady=(2, 10))

        # Recipients
        rec_frame = tk.Frame(card, bg=WHITE)
        rec_frame.pack(fill='x', padx=25, pady=(0, 10))
        tk.Label(rec_frame, text=f"{t('recipients', self.lang)} ({len(self.clients)}):",
                font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(anchor='w')
        rec_text = tk.Text(rec_frame, font=("Segoe UI", 9), height=3, bg='#f8f9fa', relief='solid', bd=1)
        recipients_str = ", ".join(f"{c.first_name} {c.last_name} <{c.email}>" for c in self.clients)
        rec_text.insert('1.0', recipients_str)
        rec_text.config(state='disabled')
        rec_text.pack(fill='x', pady=(2, 0))

        # Buttons
        btn_frame = tk.Frame(card, bg=WHITE)
        btn_frame.pack(fill='x', padx=25, pady=(0, 20))

        tk.Button(btn_frame, text=f"📤 {t('send_to_all', self.lang)}",
                 font=("Segoe UI", 11, "bold"),
                 bg=SUCCESS, fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.send).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)

        tk.Button(btn_frame, text=t('cancel', self.lang),
                 font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2', bd=0,
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def send(self):
        subject_tmpl = self.subject_entry.get()
        message_tmpl = self.message_text.get('1.0', 'end-1c')

        def get_setting(key, default=''):
            s = self.session.query(Settings).filter_by(key=key).first()
            return s.value if s else default

        mail_server = get_setting('mail_server', 'smtp.gmail.com')
        mail_port = int(get_setting('mail_port', '587'))
        mail_use_tls = get_setting('mail_use_tls', 'true') == 'true'
        mail_username = get_setting('mail_username')
        mail_password = get_setting('mail_password')
        mail_sender = get_setting('mail_default_sender', mail_username)

        if not mail_username or not mail_password:
            messagebox.showerror(t('app_name', self.lang), t('mail_not_configured', self.lang))
            return

        sent = 0
        errors = []

        try:
            with smtplib.SMTP(mail_server, mail_port) as server:
                if mail_use_tls:
                    server.starttls()
                server.login(mail_username, mail_password)

                for client in self.clients:
                    try:
                        name = f"{client.first_name} {client.last_name}"
                        subject = subject_tmpl.replace('{name}', name)
                        message = message_tmpl.replace('{name}', name)

                        msg = MIMEMultipart()
                        msg['From'] = mail_sender
                        msg['To'] = client.email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(message, 'plain'))

                        server.send_message(msg)
                        sent += 1
                    except Exception as e:
                        errors.append(f"{client.first_name} {client.last_name}: {str(e)}")
        except Exception as e:
            messagebox.showerror(t('app_name', self.lang), f"SMTP Error: {str(e)}")
            return

        result = f"Sent: {sent}/{len(self.clients)}"
        if errors:
            result += "\n\nErrors:\n" + "\n".join(errors[:5])
        messagebox.showinfo(t('app_name', self.lang), result)
        self.top.destroy()
