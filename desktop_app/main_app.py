"""
Main desktop application - Login, Dashboard, Clients, Users, Settings
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime, date
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
import uuid

from models import User, Client, Settings, init_db

# Color scheme
PRIMARY = '#ff8e00'
PRIMARY_DARK = '#e67e00'
SECONDARY = '#2ea3f2'
BG = '#f7f7f7'
TEXT = '#666666'
WHITE = '#ffffff'
DARK = '#222222'


class LoginWindow:
    """Login window"""

    def __init__(self, root, db_path, db_dir, uploads_dir):
        self.root = root
        self.db_path = db_path
        self.db_dir = db_dir
        self.uploads_dir = uploads_dir
        self.engine, self.session = init_db(db_path)

        self.root.title("Login - Jesus Projekt Erfurt")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        # Center
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 450) // 2
        y = (self.root.winfo_screenheight() - 500) // 2
        self.root.geometry(f"450x500+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(expand=True, fill='both')

        card = tk.Frame(main, bg=WHITE, bd=0, highlightthickness=1, highlightbackground='#dddddd')
        card.place(relx=0.5, rely=0.5, anchor='center', width=380, height=420)

        # Logo
        tk.Label(card, text="🎂", font=("Segoe UI Emoji", 48), bg=WHITE, fg=PRIMARY).pack(pady=(20, 5))

        # Title
        tk.Label(card, text="Jesus Projekt Erfurt", font=("Segoe UI", 18, "bold"),
                bg=WHITE, fg=PRIMARY).pack()
        tk.Label(card, text="Birthday Monitoring", font=("Segoe UI", 10),
                bg=WHITE, fg=TEXT).pack(pady=(0, 20))

        # Username
        tk.Label(card, text="Username", font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', padx=30)
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(card, textvariable=self.username_var, font=("Segoe UI", 11),
                                       relief='solid', bd=1)
        self.username_entry.pack(fill='x', padx=30, pady=(2, 12), ipady=4)

        # Password
        tk.Label(card, text="Password", font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', padx=30)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(card, textvariable=self.password_var, font=("Segoe UI", 11),
                                       show='*', relief='solid', bd=1)
        self.password_entry.pack(fill='x', padx=30, pady=(2, 20), ipady=4)

        # Login button
        self.login_btn = tk.Button(card, text="Login", font=("Segoe UI", 11, "bold"),
                                   bg=PRIMARY, fg=WHITE, activebackground=PRIMARY_DARK,
                                   activeforeground=WHITE, relief='flat', cursor='hand2',
                                   command=self.do_login)
        self.login_btn.pack(fill='x', padx=30, pady=(0, 10), ipady=8)

        # Language buttons
        lang_frame = tk.Frame(card, bg=WHITE)
        lang_frame.pack(pady=10)
        self.lang_var = tk.StringVar(value='en')
        tk.Button(lang_frame, text="English", font=("Segoe UI", 9),
                 bg=WHITE, fg=TEXT, relief='flat', cursor='hand2',
                 command=lambda: self.set_lang('en')).pack(side='left', padx=5)
        tk.Label(lang_frame, text="|", bg=WHITE, fg=TEXT).pack(side='left')
        tk.Button(lang_frame, text="Deutsch", font=("Segoe UI", 9),
                 bg=WHITE, fg=TEXT, relief='flat', cursor='hand2',
                 command=lambda: self.set_lang('de')).pack(side='left', padx=5)

        # Status
        self.status_label = tk.Label(card, text="", font=("Segoe UI", 9), bg=WHITE, fg='red')
        self.status_label.pack()

        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.do_login())
        self.username_entry.focus()

    def set_lang(self, lang):
        self.lang_var.set(lang)

    def do_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            self.status_label.config(text="Please enter username and password")
            return

        user = self.session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.is_active:
                self.status_label.config(text="Account is deactivated")
                return

            user.last_login = datetime.utcnow()
            self.session.commit()

            # Open main app
            self.root.destroy()
            main_root = tk.Tk()
            MainApp(main_root, self.db_path, self.db_dir, self.uploads_dir, user)
            main_root.mainloop()
        else:
            self.status_label.config(text="Invalid username or password")
            self.password_var.set('')


class MainApp:
    """Main application window with dashboard, clients, users, settings"""

    def __init__(self, root, db_path, db_dir, uploads_dir, current_user):
        self.root = root
        self.db_path = db_path
        self.db_dir = db_dir
        self.uploads_dir = uploads_dir
        self.engine, self.session = init_db(db_path)
        self.current_user = current_user
        self.lang = current_user.language or 'en'

        self.root.title("Jesus Projekt Erfurt - Birthday Monitoring")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG)

        # Center
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 1200) // 2
        y = (self.root.winfo_screenheight() - 700) // 2
        self.root.geometry(f"1200x700+{x}+{y}")

        self.build_ui()
        self.show_dashboard()

    def build_ui(self):
        # Top bar
        topbar = tk.Frame(self.root, bg=PRIMARY, height=60)
        topbar.pack(fill='x')
        topbar.pack_propagate(False)

        # Logo and title
        tk.Label(topbar, text="🎂 Jesus Projekt Erfurt", font=("Segoe UI", 14, "bold"),
                bg=PRIMARY, fg=WHITE).pack(side='left', padx=20, pady=15)

        # User info
        user_frame = tk.Frame(topbar, bg=PRIMARY)
        user_frame.pack(side='right', padx=20, pady=10)

        role_text = "Admin" if self.current_user.has_role('admin') else "Staff"
        tk.Label(user_frame, text=f"👤 {self.current_user.full_name} ({role_text})",
                font=("Segoe UI", 10), bg=PRIMARY, fg=WHITE).pack(side='right', padx=10)
        tk.Button(user_frame, text="Logout", font=("Segoe UI", 9),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=self.logout).pack(side='right')

        # Language switcher
        lang_frame = tk.Frame(topbar, bg=PRIMARY)
        lang_frame.pack(side='right', padx=10)
        tk.Button(lang_frame, text="EN", font=("Segoe UI", 9),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=lambda: self.switch_lang('en')).pack(side='left')
        tk.Button(lang_frame, text="DE", font=("Segoe UI", 9),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=lambda: self.switch_lang('de')).pack(side='left')

        # Sidebar
        sidebar = tk.Frame(self.root, bg=DARK, width=200)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)

        # Menu buttons
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("👥 Clients", self.show_clients),
        ]
        if self.current_user.has_role('admin'):
            menu_items.append(("👤 Users", self.show_users))
            menu_items.append(("⚙️ Settings", self.show_settings))
        menu_items.append(("👤 My Profile", self.show_profile))

        for text, command in menu_items:
            btn = tk.Button(sidebar, text=text, font=("Segoe UI", 11),
                          bg=DARK, fg=WHITE, activebackground=PRIMARY,
                          activeforeground=WHITE, relief='flat', cursor='hand2',
                          anchor='w', padx=20, command=command)
            btn.pack(fill='x', pady=2, ipady=10)

        # Content area
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side='left', fill='both', expand=True)

    def switch_lang(self, lang):
        self.lang = lang
        self.current_user.language = lang
        self.session.commit()
        self.refresh_content()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def refresh_content(self):
        # Just clear and re-show current view
        self.clear_content()
        # Simple approach: rebuild UI
        # For now, just go to dashboard
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_content()

        # Header
        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(header, text="Dashboard", font=("Segoe UI", 20, "bold"),
                bg=BG, fg=DARK).pack(side='left')

        # Stats cards
        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill='x', padx=20)

        total_clients = self.session.query(Client).count()
        today_birthdays = self.session.query(Client).filter(
            Client.birthday.like(f'%-{date.today().strftime("%m-%d")}')
        ).count()

        self.create_stat_card(stats, "Total Clients", str(total_clients), PRIMARY).pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.create_stat_card(stats, "Today's Birthdays", str(today_birthdays), SECONDARY).pack(side='left', padx=5, pady=5, fill='x', expand=True)

        # Month selector
        month_frame = tk.Frame(self.content, bg=WHITE, bd=1, relief='solid')
        month_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(month_frame, text="Birthday Celebrants", font=("Segoe UI", 14, "bold"),
                bg=WHITE, fg=DARK).pack(anchor='w', padx=15, pady=(15, 5))

        select_frame = tk.Frame(month_frame, bg=WHITE)
        select_frame.pack(fill='x', padx=15, pady=10)

        months_en = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
        months_de = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                    'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
        months = months_de if self.lang == 'de' else months_en

        tk.Label(select_frame, text="Select Month:", font=("Segoe UI", 10),
                bg=WHITE).pack(side='left', padx=(0, 10))
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(select_frame, textvariable=self.month_var,
                                   values=['All'] + months, state='readonly', width=20)
        month_combo.set('All')
        month_combo.pack(side='left', padx=(0, 10))
        month_combo.bind('<<ComboboxSelected>>', lambda e: self.load_birthday_list(month_combo))

        # Send Greetings button
        tk.Button(select_frame, text="📧 Send Greetings", font=("Segoe UI", 10, "bold"),
                 bg='#28a745', fg=WHITE, relief='flat', cursor='hand2',
                 command=self.open_send_greetings).pack(side='right')

        # Table
        table_frame = tk.Frame(month_frame, bg=WHITE)
        table_frame.pack(fill='both', expand=True, padx=15, pady=10)

        columns = ('Name', 'Birthday', 'Age', 'Phone', 'Email', 'Privacy', 'Photo')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.load_birthday_list(month_combo)

    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=color, bd=0)
        content = tk.Frame(card, bg=color)
        content.pack(padx=20, pady=15, fill='both', expand=True)
        tk.Label(content, text=title, font=("Segoe UI", 11), bg=color, fg=WHITE).pack(anchor='w')
        tk.Label(content, text=value, font=("Segoe UI", 28, "bold"), bg=color, fg=WHITE).pack(anchor='w')
        return card

    def load_birthday_list(self, month_combo):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected = month_combo.get()
        query = self.session.query(Client)

        if selected != 'All':
            months_en = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
            months_de = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                        'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
            months = months_de if self.lang == 'de' else months_en
            month_num = months.index(selected) + 1
            query = query.filter(
                Client.birthday.like(f'%-{month_num:02d}-%')
            )

        clients = query.order_by(Client.birthday).all()
        for c in clients:
            self.tree.insert('', 'end', values=(
                f"{c.first_name} {c.last_name}",
                c.birthday.strftime('%d.%m.%Y'),
                c.age,
                c.phone or '-',
                c.email or '-',
                '✓' if c.privacy_signed else '✗',
                '✓' if c.photo_permission else '✗'
            ))

    def show_clients(self):
        self.clear_content()

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=20)
        tk.Label(header, text="Clients", font=("Segoe UI", 20, "bold"),
                bg=BG, fg=DARK).pack(side='left')
        tk.Button(header, text="➕ Add Client", font=("Segoe UI", 10, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=self.open_add_client).pack(side='right')

        # Table
        table_frame = tk.Frame(self.content, bg=WHITE, bd=1, relief='solid')
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ('Name', 'Birthday', 'Age', 'Phone', 'Email', 'Actions')
        self.client_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        for col in columns:
            self.tree_heading = self.client_tree.heading(col, text=col)
            if col == 'Actions':
                self.client_tree.column(col, width=150)
            else:
                self.client_tree.column(col, width=150)

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
                actions = "Edit | Delete" if self.current_user.has_role('admin') else "Edit"
                self.client_tree.insert('', 'end', iid=c.id, values=(
                    f"{c.first_name} {c.last_name}",
                    c.birthday.strftime('%d.%m.%Y'),
                    c.age,
                    c.phone or '-',
                    c.email or '-',
                    actions
                ))

    def edit_client_event(self, event):
        item = self.client_tree.selection()
        if item:
            client_id = int(item[0])
            self.open_edit_client(client_id)

    def open_add_client(self):
        ClientDialog(self.root, self.session, self.load_clients)

    def open_edit_client(self, client_id):
        client = self.session.query(Client).get(client_id)
        if client:
            ClientDialog(self.root, self.session, self.load_clients, client)

    def show_users(self):
        if not self.current_user.has_role('admin'):
            return
        self.clear_content()

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=20)
        tk.Label(header, text="User Management", font=("Segoe UI", 20, "bold"),
                bg=BG, fg=DARK).pack(side='left')
        tk.Button(header, text="➕ Add User", font=("Segoe UI", 10, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=self.open_add_user).pack(side='right')

        # Table
        table_frame = tk.Frame(self.content, bg=WHITE, bd=1, relief='solid')
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ('Username', 'Email', 'Name', 'Role', 'Status', 'Actions')
        self.user_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        for col in columns:
            self.user_tree.heading(col, text=col)
            if col == 'Actions':
                self.user_tree.column(col, width=150)
            else:
                self.user_tree.column(col, width=150)

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
                    u.username,
                    u.email,
                    u.full_name,
                    u.role,
                    'Active' if u.is_active else 'Inactive',
                    'Edit | Delete' if u.id != self.current_user.id else 'Edit'
                ))

    def edit_user_event(self, event):
        item = self.user_tree.selection()
        if item:
            user_id = int(item[0])
            self.open_edit_user(user_id)

    def open_add_user(self):
        UserDialog(self.root, self.session, self.uploads_dir, self.load_users, is_admin=self.current_user.has_role('admin'))

    def open_edit_user(self, user_id):
        user = self.session.query(User).get(user_id)
        if user:
            UserDialog(self.root, self.session, self.uploads_dir, self.load_users, user, is_admin=self.current_user.has_role('admin'))

    def show_settings(self):
        if not self.current_user.has_role('admin'):
            return
        self.clear_content()

        header = tk.Frame(self.content, bg=BG)
        header.pack(fill='x', padx=20, pady=20)
        tk.Label(header, text="Email Settings", font=("Segoe UI", 20, "bold"),
                bg=BG, fg=DARK).pack(side='left')

        # Form
        form_frame = tk.Frame(self.content, bg=WHITE, bd=1, relief='solid')
        form_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Get current settings
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
            ("SMTP Server", self.smtp_server_var, 'entry'),
            ("SMTP Port", self.smtp_port_var, 'entry'),
            ("Email Address", self.smtp_username_var, 'entry'),
            ("App Password", self.smtp_password_var, 'entry'),
            ("Sender Address", self.smtp_sender_var, 'entry'),
        ]

        row = 0
        for label, var, ftype in fields:
            tk.Label(form_frame, text=label, font=("Segoe UI", 10), bg=WHITE,
                    anchor='w').grid(row=row, column=0, sticky='w', padx=20, pady=10)
            entry = tk.Entry(form_frame, textvariable=var, font=("Segoe UI", 11), width=40)
            if 'Password' in label:
                entry.config(show='*')
            entry.grid(row=row, column=1, sticky='ew', padx=20, pady=10)
            row += 1

        tk.Label(form_frame, text="Use TLS", font=("Segoe UI", 10), bg=WHITE).grid(row=row, column=0, sticky='w', padx=20, pady=10)
        tk.Checkbutton(form_frame, variable=self.smtp_tls_var, bg=WHITE).grid(row=row, column=1, sticky='w', padx=20, pady=10)
        row += 1

        form_frame.columnconfigure(1, weight=1)

        tk.Button(form_frame, text="Save Settings", font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
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
            self.session.commit()

        set_setting('mail_server', self.smtp_server_var.get())
        set_setting('mail_port', self.smtp_port_var.get())
        set_setting('mail_username', self.smtp_username_var.get())
        set_setting('mail_password', self.smtp_password_var.get())
        set_setting('mail_default_sender', self.smtp_sender_var.get())
        set_setting('mail_use_tls', 'true' if self.smtp_tls_var.get() else 'false')

        messagebox.showinfo("Success", "Settings saved successfully!")

    def show_profile(self):
        self.clear_content()
        ProfileDialog(self.root, self.session, self.uploads_dir, self)

    def open_send_greetings(self):
        selected = self.month_var.get()
        if selected == 'All':
            months_en = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
            months_de = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                        'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
            months = months_de if self.lang == 'de' else months_en
            month_num = months.index(selected) + 1
        else:
            months_en = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
            months_de = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                        'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
            months = months_de if self.lang == 'de' else months_en
            month_num = months.index(selected) + 1

        clients = self.session.query(Client).filter(
            Client.birthday.like(f'%-{month_num:02d}-%'),
            Client.email.isnot(None),
            Client.email != ''
        ).all()

        if not clients:
            messagebox.showwarning("No Recipients", "No clients with email addresses for this month.")
            return

        GreetingDialog(self.root, self.session, clients, self)

    def logout(self):
        self.root.destroy()
        login_root = tk.Tk()
        LoginWindow(login_root, self.db_path, self.db_dir, self.uploads_dir)
        login_root.mainloop()


class ClientDialog:
    """Add/Edit client dialog"""
    def __init__(self, parent, session, refresh_callback, client=None):
        self.session = session
        self.refresh_callback = refresh_callback
        self.client = client

        self.top = tk.Toplevel(parent)
        self.top.title("Add Client" if client is None else "Edit Client")
        self.top.geometry("500x600")
        self.top.configure(bg=WHITE)
        self.top.transient(parent)
        self.top.grab_set()

        # Center
        self.top.update_idletasks()
        x = (parent.winfo_screenwidth() - 500) // 2
        y = (parent.winfo_screenheight() - 600) // 2
        self.top.geometry(f"500x600+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.top, text="Add Client" if self.client is None else "Edit Client",
                font=("Segoe UI", 16, "bold"), bg=WHITE, fg=PRIMARY).pack(pady=20)

        # Form
        form = tk.Frame(self.top, bg=WHITE)
        form.pack(fill='both', expand=True, padx=30)

        self.first_name_var = tk.StringVar(value=self.client.first_name if self.client else '')
        self.last_name_var = tk.StringVar(value=self.client.last_name if self.client else '')
        self.address_var = tk.StringVar(value=self.client.address if self.client else '')
        self.phone_var = tk.StringVar(value=self.client.phone if self.client else '')
        self.email_var = tk.StringVar(value=self.client.email if self.client else '')
        self.privacy_var = tk.BooleanVar(value=self.client.privacy_signed if self.client else False)
        self.photo_var = tk.BooleanVar(value=self.client.photo_permission if self.client else False)

        fields = [
            ("First Name *", self.first_name_var),
            ("Last Name *", self.last_name_var),
            ("Address", self.address_var),
            ("Phone", self.phone_var),
            ("Email", self.email_var),
        ]

        for label, var in fields:
            tk.Label(form, text=label, font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(5, 0))
            entry = tk.Entry(form, textvariable=var, font=("Segoe UI", 11))
            entry.pack(fill='x', pady=(2, 10), ipady=4)

        tk.Label(form, text="Birthday *", font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(5, 0))
        self.birthday_entry = tk.Entry(form, font=("Segoe UI", 11))
        if self.client:
            self.birthday_entry.insert(0, self.client.birthday.strftime('%Y-%m-%d'))
        else:
            self.birthday_entry.insert(0, 'YYYY-MM-DD')
        self.birthday_entry.pack(fill='x', pady=(2, 10), ipady=4)

        tk.Checkbutton(form, text="Privacy Signed", variable=self.privacy_var, bg=WHITE).pack(anchor='w', pady=5)
        tk.Checkbutton(form, text="Photo Permission", variable=self.photo_var, bg=WHITE).pack(anchor='w', pady=5)

        # Buttons
        btn_frame = tk.Frame(self.top, bg=WHITE)
        btn_frame.pack(fill='x', padx=30, pady=20)

        tk.Button(btn_frame, text="Save", font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=self.save).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)
        tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2',
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def save(self):
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        birthday_str = self.birthday_entry.get().strip()

        if not first_name or not last_name or not birthday_str or birthday_str == 'YYYY-MM-DD':
            messagebox.showerror("Error", "First name, last name, and birthday are required.")
            return

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
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

        self.session.commit()
        self.refresh_callback()
        self.top.destroy()


class UserDialog:
    """Add/Edit user dialog"""
    def __init__(self, parent, session, uploads_dir, refresh_callback, user=None, is_admin=False):
        self.session = session
        self.uploads_dir = uploads_dir
        self.refresh_callback = refresh_callback
        self.user = user
        self.is_admin = is_admin
        self.profile_picture_path = None

        self.top = tk.Toplevel(parent)
        self.top.title("Add User" if user is None else "Edit User")
        self.top.geometry("500x700")
        self.top.configure(bg=WHITE)
        self.top.transient(parent)
        self.top.grab_set()

        self.top.update_idletasks()
        x = (parent.winfo_screenwidth() - 500) // 2
        y = (parent.winfo_screenheight() - 700) // 2
        self.top.geometry(f"500x700+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        tk.Label(self.top, text="Add User" if self.user is None else "Edit User",
                font=("Segoe UI", 16, "bold"), bg=WHITE, fg=PRIMARY).pack(pady=20)

        form = tk.Frame(self.top, bg=WHITE)
        form.pack(fill='both', expand=True, padx=30)

        self.username_var = tk.StringVar(value=self.user.username if self.user else '')
        self.email_var = tk.StringVar(value=self.user.email if self.user else '')
        self.first_name_var = tk.StringVar(value=self.user.first_name if self.user else '')
        self.last_name_var = tk.StringVar(value=self.user.last_name if self.user else '')
        self.role_var = tk.StringVar(value=self.user.role if self.user else 'staff')
        self.active_var = tk.BooleanVar(value=self.user.is_active if self.user else True)

        fields = [
            ("Username *", self.username_var),
            ("Email *", self.email_var),
            ("First Name", self.first_name_var),
            ("Last Name", self.last_name_var),
        ]

        for label, var in fields:
            tk.Label(form, text=label, font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(5, 0))
            tk.Entry(form, textvariable=var, font=("Segoe UI", 11)).pack(fill='x', pady=(2, 10), ipady=4)

        tk.Label(form, text="Password" + ("" if self.user else " *"), font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(5, 0))
        self.password_entry = tk.Entry(form, font=("Segoe UI", 11), show='*')
        if not self.user:
            self.password_entry.pack(fill='x', pady=(2, 10), ipady=4)
        else:
            self.password_entry.pack(fill='x', pady=(2, 5), ipady=4)
            tk.Label(form, text="Leave blank to keep current", font=("Segoe UI", 8),
                    bg=WHITE, fg=TEXT).pack(anchor='w')

        if self.is_admin:
            tk.Label(form, text="Role", font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(5, 0))
            role_combo = ttk.Combobox(form, textvariable=self.role_var, values=['staff', 'admin'], state='readonly')
            role_combo.pack(fill='x', pady=(2, 10), ipady=4)

            tk.Checkbutton(form, text="Active", variable=self.active_var, bg=WHITE).pack(anchor='w', pady=5)

        # Profile picture
        pic_frame = tk.Frame(form, bg=WHITE)
        pic_frame.pack(fill='x', pady=10)
        self.pic_label = tk.Label(pic_frame, text="No picture", bg='#dddddd', width=10, height=5)
        self.pic_label.pack(side='left', padx=(0, 10))
        tk.Button(pic_frame, text="Upload Photo", command=self.upload_photo).pack(side='left')

        if self.user and self.user.profile_picture:
            self.load_user_picture()

        # Buttons
        btn_frame = tk.Frame(self.top, bg=WHITE)
        btn_frame.pack(fill='x', padx=30, pady=20)

        tk.Button(btn_frame, text="Save", font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=self.save).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)
        tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2',
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def upload_photo(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if filename:
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
            print(f"Error loading image: {e}")

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
            messagebox.showerror("Error", "Username and email are required.")
            return

        if not self.user and not password:
            messagebox.showerror("Error", "Password is required for new users.")
            return

        # Check duplicates
        if not self.user:
            if self.session.query(User).filter_by(username=username).first():
                messagebox.showerror("Error", "Username already exists.")
                return
            if self.session.query(User).filter_by(email=email).first():
                messagebox.showerror("Error", "Email already exists.")
                return

        if self.user:
            self.user.username = username
            self.user.email = email
            self.user.first_name = self.first_name_var.get().strip()
            self.user.last_name = self.last_name_var.get().strip()
            if self.is_admin:
                self.user.role = self.role_var.get()
                self.user.is_active = self.active_var.get()
            if password:
                self.user.set_password(password)
        else:
            user = User(
                username=username,
                email=email,
                first_name=self.first_name_var.get().strip(),
                last_name=self.last_name_var.get().strip(),
                role=self.role_var.get() if self.is_admin else 'staff',
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
        self.refresh_callback()
        self.top.destroy()


class ProfileDialog:
    """User profile dialog"""
    def __init__(self, parent, session, uploads_dir, main_app):
        self.session = session
        self.uploads_dir = uploads_dir
        self.main_app = main_app
        self.user = main_app.current_user
        self.profile_picture_path = None

        self.top = tk.Toplevel(parent)
        self.top.title("My Profile")
        self.top.geometry("500x600")
        self.top.configure(bg=WHITE)
        self.top.transient(parent)
        self.top.grab_set()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.top, text="My Profile", font=("Segoe UI", 16, "bold"),
                bg=WHITE, fg=PRIMARY).pack(pady=20)

        form = tk.Frame(self.top, bg=WHITE)
        form.pack(fill='both', expand=True, padx=30)

        self.username_var = tk.StringVar(value=self.user.username)
        self.email_var = tk.StringVar(value=self.user.email)
        self.first_name_var = tk.StringVar(value=self.user.first_name or '')
        self.last_name_var = tk.StringVar(value=self.user.last_name or '')

        fields = [
            ("Username *", self.username_var),
            ("Email *", self.email_var),
            ("First Name", self.first_name_var),
            ("Last Name", self.last_name_var),
        ]

        for label, var in fields:
            tk.Label(form, text=label, font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(5, 0))
            tk.Entry(form, textvariable=var, font=("Segoe UI", 11)).pack(fill='x', pady=(2, 10), ipady=4)

        tk.Label(form, text="New Password", font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x', pady=(5, 0))
        self.password_entry = tk.Entry(form, font=("Segoe UI", 11), show='*')
        self.password_entry.pack(fill='x', pady=(2, 5), ipady=4)
        tk.Label(form, text="Leave blank to keep current", font=("Segoe UI", 8),
                bg=WHITE, fg=TEXT).pack(anchor='w')

        # Profile picture
        pic_frame = tk.Frame(form, bg=WHITE)
        pic_frame.pack(fill='x', pady=10)
        self.pic_label = tk.Label(pic_frame, text="No picture", bg='#dddddd', width=10, height=5)
        self.pic_label.pack(side='left', padx=(0, 10))
        tk.Button(pic_frame, text="Upload Photo", command=self.upload_photo).pack(side='left')

        if self.user.profile_picture:
            self.load_user_picture()

        # Buttons
        btn_frame = tk.Frame(self.top, bg=WHITE)
        btn_frame.pack(fill='x', padx=30, pady=20)

        tk.Button(btn_frame, text="Save", font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY, fg=WHITE, relief='flat', cursor='hand2',
                 command=self.save).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)
        tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2',
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def upload_photo(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if filename:
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
        messagebox.showinfo("Success", "Profile updated successfully!")
        self.top.destroy()


class GreetingDialog:
    """Send birthday greetings dialog"""
    def __init__(self, parent, session, clients, main_app):
        self.session = session
        self.clients = clients
        self.main_app = main_app

        self.top = tk.Toplevel(parent)
        self.top.title("Send Birthday Greetings")
        self.top.geometry("600x500")
        self.top.configure(bg=WHITE)
        self.top.transient(parent)
        self.top.grab_set()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.top, text="Send Birthday Greetings", font=("Segoe UI", 16, "bold"),
                bg=WHITE, fg=PRIMARY).pack(pady=20)

        tk.Label(self.top, text=f"Recipients: {len(self.clients)}",
                font=("Segoe UI", 10), bg=WHITE, fg=TEXT).pack()

        form = tk.Frame(self.top, bg=WHITE)
        form.pack(fill='both', expand=True, padx=30, pady=10)

        tk.Label(form, text="Subject", font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x')
        self.subject_entry = tk.Entry(form, font=("Segoe UI", 11))
        self.subject_entry.insert(0, "Happy Birthday, {name}!")
        self.subject_entry.pack(fill='x', pady=(2, 10), ipady=4)

        tk.Label(form, text="Message", font=("Segoe UI", 10), bg=WHITE, anchor='w').pack(fill='x')
        self.message_text = tk.Text(form, font=("Segoe UI", 10), height=12, wrap='word')
        self.message_text.insert('1.0',
            "Dear {name},\n\nWishing you a wonderful birthday! May this special day bring you joy and happiness.\n\nFrom all of us at Jesus Projekt Erfurt!\n\nBest regards,\nJesus Projekt Erfurt Team")
        self.message_text.pack(fill='both', expand=True, pady=(2, 10))

        btn_frame = tk.Frame(self.top, bg=WHITE)
        btn_frame.pack(fill='x', padx=30, pady=20)

        tk.Button(btn_frame, text="Send", font=("Segoe UI", 11, "bold"),
                 bg='#28a745', fg=WHITE, relief='flat', cursor='hand2',
                 command=self.send).pack(side='left', fill='x', expand=True, padx=(0, 5), ipady=8)
        tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 11),
                 bg='#6c757d', fg=WHITE, relief='flat', cursor='hand2',
                 command=self.top.destroy).pack(side='right', fill='x', expand=True, padx=(5, 0), ipady=8)

    def send(self):
        subject_tmpl = self.subject_entry.get()
        message_tmpl = self.message_text.get('1.0', 'end-1c')

        # Get settings
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
            messagebox.showerror("Error", "Email not configured. Please set up email in Settings.")
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
            messagebox.showerror("Error", f"SMTP connection failed: {str(e)}")
            return

        result = f"Sent: {sent}\nFailed: {len(errors)}"
        if errors:
            result += "\n\nErrors:\n" + "\n".join(errors[:5])
        messagebox.showinfo("Complete", result)
        self.top.destroy()
