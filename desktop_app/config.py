"""
Jesus Projekt Erfurt - Birthday Monitoring
Desktop Application - Pure tkinter, no browser needed
Matches the web version (run.bat) design exactly.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
from datetime import datetime, date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
import uuid
import csv

from models import User, Client, Settings, init_db

# ==================== CONFIGURATION ====================

# Color scheme - matches web version CSS exactly
PRIMARY = '#ff8e00'
PRIMARY_DARK = '#e67e00'
SECONDARY = '#2ea3f2'
BG = '#f7f7f7'
TEXT = '#666666'
TEXT_DARK = '#333333'
WHITE = '#ffffff'
DARK = '#222222'
SUCCESS = '#28a745'
DANGER = '#dc3545'
WARNING = '#ffc107'
BORDER = '#e0e0e0'
INPUT_BG = '#ffffff'
INPUT_BORDER = '#ced4da'

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

# Database locations
EXE_DB_PATH = os.path.join(APP_DIR, 'birthday_monitoring.db')
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Jesus Projekt Erfurt')
APPDATA_DB_PATH = os.path.join(APPDATA_DIR, 'birthday_monitoring.db')

UPLOADS_DIR = os.path.join(APP_DIR, 'uploads')
APPDATA_UPLOADS = os.path.join(APPDATA_DIR, 'uploads')

# Logo paths - official Jesus Projekt Erfurt logo
LOGO_URL = 'https://jesus-projekt-erfurt.de/wp-content/uploads/2017/03/Jesus-Projekt-Erfurt-Logo.jpg'
LOCAL_LOGO = os.path.join(APP_DIR, 'logo.jpg')
BUNDLED_LOGO = os.path.join(BASE_DIR, 'logo.jpg') if BASE_DIR != APP_DIR else None
ICON_PATH = os.path.join(APP_DIR, 'app.ico')
BUNDLED_ICON = os.path.join(BASE_DIR, 'app.ico') if BASE_DIR != APP_DIR else None

# Fonts
FONT_FAMILY = 'Segoe UI'
FONT_EMOJI = 'Segoe UI Emoji'


# ==================== TRANSLATIONS (exact copy from web version) ====================

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
        'today_birthdays': "Today's Birthdays",
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
        'greetings_sent': 'Birthday greetings sent successfully!',
        'greeting_error': 'Error sending greetings.',
        'no_email_clients': 'No clients with email addresses found.',
        'recipients': 'Recipients',
        'subject': 'Subject',
        'message': 'Message',
        'placeholders_info': 'Use {name} for client name, {first_name} for first name, {last_name} for last name',
        'mail_not_configured': 'Email is not configured. Please go to Settings.',
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
        'leave_blank_no_change': 'Leave blank to keep current',
        'admin_actions': 'Admin Actions',
        'reset_password': 'Reset Password',
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
        'today_birthdays': 'Heutige Geburtstage',
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
        'greetings_sent': 'Geburtstagsgrüße erfolgreich gesendet!',
        'greeting_error': 'Fehler beim Senden.',
        'no_email_clients': 'Keine Kunden mit E-Mail-Adressen gefunden.',
        'recipients': 'Empfänger',
        'subject': 'Betreff',
        'message': 'Nachricht',
        'placeholders_info': 'Verwenden Sie {name} für den Namen, {first_name} für Vorname, {last_name} für Nachname',
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
        'leave_blank_no_change': 'Leer lassen um aktuelles zu behalten',
        'admin_actions': 'Admin-Aktionen',
        'reset_password': 'Passwort zurücksetzen',
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


# ==================== UTILITY FUNCTIONS ====================

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
    if BUNDLED_ICON and os.path.exists(BUNDLED_ICON):
        return BUNDLED_ICON
    if os.path.exists(ICON_PATH):
        return ICON_PATH
    return ICON_PATH


def get_logo_path():
    """Get the official Jesus Projekt Erfurt logo"""
    # Try bundled first (inside exe)
    if BUNDLED_LOGO and os.path.exists(BUNDLED_LOGO):
        return BUNDLED_LOGO
    # Then APP_DIR
    if os.path.exists(LOCAL_LOGO):
        return LOCAL_LOGO
    return None


def get_logo_image(size=(200, 100)):
    """Load and resize the official Jesus Projekt Erfurt logo"""
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
