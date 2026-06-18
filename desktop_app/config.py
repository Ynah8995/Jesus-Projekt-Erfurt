"""
Jesus Projekt Erfurt - Birthday Monitoring
Constants and configuration shared across modules
"""
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ==================== CONFIGURATION ====================

# Color scheme - matches web version CSS exactly
PRIMARY = '#ff8e00'
PRIMARY_DARK = '#e67e00'
PRIMARY_HOVER = '#cc7a00'
SECONDARY = '#2ea3f2'
SECONDARY_DARK = '#1e8acb'
BG = '#f7f7f7'
BG_LIGHT = '#fafafa'
TEXT = '#666666'
TEXT_DARK = '#333333'
WHITE = '#ffffff'
DARK = '#222222'
SUCCESS = '#28a745'
SUCCESS_DARK = '#218838'
DANGER = '#dc3545'
DANGER_DARK = '#c82333'
WARNING = '#ffc107'
INFO = '#17a2b8'
BORDER = '#e0e0e0'
INPUT_BG = '#ffffff'
INPUT_BORDER = '#ced4da'

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

# Logo paths
LOCAL_LOGO = os.path.join(APP_DIR, 'logo.jpg')
LOGO_URL = 'https://jesus-projekt-erfurt.de/wp-content/uploads/2017/03/Jesus-Projekt-Erfurt-Logo.jpg'
ICON_PATH = os.path.join(APP_DIR, 'app.ico')

# Fonts
FONT_FAMILY = 'Segoe UI'
FONT_LOGO_EMOJI = 'Segoe UI Emoji'


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
        'delete_client': 'Delete Client',
        'select_month': 'Select Month',
        'all_months': 'All Months',
        'birthday_celebrants': 'Birthday Celebrants',
        'no_celebrants': 'No birthday celebrants found for this month.',
        'no_clients': 'No clients found. Click "Add Client" to get started.',
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
        'sending': 'Sending...',
        'greetings_sent': 'Birthday greetings sent successfully!',
        'greeting_error': 'Error sending greetings. Please try again.',
        'no_email_clients': 'No clients with email addresses found.',
        'recipients': 'Recipients',
        'subject': 'Subject',
        'message': 'Message',
        'placeholders_info': 'Use {name} for client name, {first_name} for first name, {last_name} for last name',
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
        'export_csv': 'Export to CSV',
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
        'no_clients': 'Keine Kunden gefunden. Klicken Sie auf "Kunde hinzufügen" um zu beginnen.',
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
        'sending': 'Wird gesendet...',
        'greetings_sent': 'Geburtstagsgrüße erfolgreich gesendet!',
        'greeting_error': 'Fehler beim Senden. Bitte versuchen Sie es erneut.',
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
        'export_csv': 'Als CSV exportieren',
    }
}


def t(key, lang='en'):
    """Get translation for key"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)


# ==================== UTILITY FUNCTIONS ====================

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
    """Get database path - try exe folder first, fallback to AppData"""
    if can_write_to(APP_DIR):
        return EXE_DB_PATH, APP_DIR, UPLOADS_DIR
    else:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        os.makedirs(APPDATA_UPLOADS, exist_ok=True)
        return APPDATA_DB_PATH, APPDATA_DIR, APPDATA_UPLOADS


def get_icon_path():
    """Get the icon file path"""
    if os.path.exists(ICON_PATH):
        return ICON_PATH
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'app.ico')
    return ICON_PATH


def get_logo_image(size=(150, 80)):
    """Load and resize the logo image"""
    # Try local file first
    if os.path.exists(LOCAL_LOGO):
        try:
            img = Image.open(LOCAL_LOGO)
            img.thumbnail(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            pass

    # Try to download
    try:
        import urllib.request
        urllib.request.urlretrieve(LOGO_URL, LOCAL_LOGO)
        img = Image.open(LOCAL_LOGO)
        img.thumbnail(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        pass

    return None


def apply_window_icon(window):
    """Apply the app icon to a window"""
    try:
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            window.iconbitmap(icon_path)
    except Exception:
        pass


def center_window(window, width, height):
    """Center a window on screen"""
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
