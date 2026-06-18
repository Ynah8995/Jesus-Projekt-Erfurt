"""
First-time setup script
Creates the first admin user when the database is empty.
Run this once after the first launch of the .exe, or before launching it.

Usage:
    python first_setup.py
"""
import os
import sys
import getpass

# Get database path (same logic as main app)
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

EXE_DB_PATH = os.path.join(APP_DIR, 'birthday_monitoring.db')
APPDATA_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Jesus Projekt Erfurt')
APPDATA_DB_PATH = os.path.join(APPDATA_DIR, 'birthday_monitoring.db')


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
        return EXE_DB_PATH
    else:
        os.makedirs(APPDATA_DIR, exist_ok=True)
        return APPDATA_DB_PATH


def main():
    from models import init_db, User
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    db_path = get_db_path()
    print(f"Database location: {db_path}")

    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    from models import Base
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if any users exist
    existing = session.query(User).first()
    if existing:
        print(f"\nUsers already exist in the database.")
        print(f"Existing users: {session.query(User).count()}")
        create = input("Create another admin user? (y/n): ").strip().lower()
        if create != 'y':
            print("Exiting.")
            return

    print("\n=== Create Admin User ===")
    username = input("Username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    email = input("Email: ").strip()
    if not email:
        print("Email cannot be empty.")
        return

    first_name = input("First name (optional): ").strip()
    last_name = input("Last name (optional): ").strip()

    while True:
        password = getpass.getpass("Password: ")
        if len(password) < 4:
            print("Password must be at least 4 characters.")
            continue
        password2 = getpass.getpass("Confirm password: ")
        if password != password2:
            print("Passwords do not match.")
            continue
        break

    # Check for duplicates
    if session.query(User).filter_by(username=username).first():
        print(f"Error: Username '{username}' already exists.")
        return
    if session.query(User).filter_by(email=email).first():
        print(f"Error: Email '{email}' already exists.")
        return

    user = User(
        username=username,
        email=email,
        first_name=first_name or None,
        last_name=last_name or None,
        role='admin',
        is_active=True,
        language='en'
    )
    user.set_password(password)
    session.add(user)
    session.commit()

    print(f"\n✓ Admin user '{username}' created successfully!")
    print(f"You can now log in to the application with these credentials.")


if __name__ == '__main__':
    main()
