"""Build script for creating the .exe"""
import os
import sys
import shutil
import subprocess

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

print("=" * 60)
print("Jesus Projekt Erfurt - Build Script")
print("=" * 60)
print(f"Project directory: {PROJECT_DIR}")
print(f"Build directory: {SCRIPT_DIR}")

# Step 1: Copy web app files to desktop_app/app_web/app/
app_web_dir = os.path.join(SCRIPT_DIR, 'app_web', 'app')
app_src_dir = os.path.join(PROJECT_DIR, 'app')

print(f"\nCopying web app from {app_src_dir} to {app_web_dir}...")

# Clean and recreate
if os.path.exists(os.path.join(SCRIPT_DIR, 'app_web')):
    shutil.rmtree(os.path.join(SCRIPT_DIR, 'app_web'))
os.makedirs(app_web_dir, exist_ok=True)

# Copy all files from app/ to app_web/app/
for item in os.listdir(app_src_dir):
    src = os.path.join(app_src_dir, item)
    dst = os.path.join(app_web_dir, item)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)

print("Web app copied successfully.")

# Step 2: Build with PyInstaller
print("\nBuilding .exe with PyInstaller...")
os.chdir(SCRIPT_DIR)

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--windowed',
    '--name', 'Jesus Projekt Erfurt',
    '--icon', 'app.ico',
    '--add-data', 'app_web/app;app',
    '--add-data', 'app_web/app/templates;app/templates',
    '--add-data', 'app_web/app/static;app/static',
    '--collect-all', 'webview',
    '--noconfirm',
    '--clean',
    'app.py'
]

print("Command:", ' '.join(cmd))
result = subprocess.run(cmd)
if result.returncode != 0:
    print("Build failed!")
    sys.exit(1)

# Step 3: Verify
exe_path = os.path.join(SCRIPT_DIR, 'dist', 'Jesus Projekt Erfurt.exe')
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\nBuild successful!")
    print(f"Executable: {exe_path}")
    print(f"Size: {size_mb:.1f} MB")
else:
    print("Build failed - executable not found")
    sys.exit(1)
