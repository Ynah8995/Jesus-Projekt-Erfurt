"""
Build script for creating .exe with PyInstaller
Run: python build.py
"""
import os
import subprocess
import sys


def install_dependencies():
    """Install required packages"""
    packages = [
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'pyinstaller',
        'pillow',
    ]
    for pkg in packages:
        print(f"Installing {pkg}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True)


def build_exe():
    """Build the .exe with PyInstaller"""
    print("Building .exe...")

    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',           # Single file
        '--windowed',          # No console window
        '--name', 'Jesus Projekt Erfurt',
        '--icon', 'NONE',      # Add icon if available
        '--add-data', 'app.py;.',
        'app.py'
    ]

    subprocess.run(cmd, check=True)
    print("\nBuild complete!")
    print(f"Executable: {os.path.join('dist', 'Jesus Projekt Erfurt.exe')}")


if __name__ == '__main__':
    install_dependencies()
    build_exe()
