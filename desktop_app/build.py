"""Build script for creating the .exe with Flask web app in WebView2 window"""
import os
import sys
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

print("=" * 60)
print("Jesus Projekt Erfurt - Build Script")
print("=" * 60)
print(f"Project: {PROJECT_DIR}")
print(f"Build: {SCRIPT_DIR}")

# Clean previous build
for item in ['dist', 'build', 'webapp']:
    path = os.path.join(SCRIPT_DIR, item)
    if os.path.exists(path):
        print(f"Cleaning {path}...")
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"  Warning: {e}")
for spec_file in ['app.spec']:
    path = os.path.join(SCRIPT_DIR, spec_file)
    if os.path.exists(path):
        os.remove(path)

# Step 1: Copy web app to webapp/ folder
print("\n[1/2] Copying web app files...")
app_src = os.path.join(PROJECT_DIR, 'app')
webapp_dst = os.path.join(SCRIPT_DIR, 'webapp')
os.makedirs(webapp_dst, exist_ok=True)
shutil.copytree(app_src, os.path.join(webapp_dst, 'app'))
print(f"Copied {app_src} to {webapp_dst}")

# Step 2: Build with PyInstaller
print("\n[2/2] Building .exe...")
os.chdir(SCRIPT_DIR)

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile', '--windowed',
    '--name', 'Jesus Projekt Erfurt',
    '--icon', 'app.ico',
    '--add-data', 'app.ico;.',
    '--add-data', 'logo.jpg;.',
    '--add-data', 'webapp/app;app',
    '--add-data', 'webapp/app/templates;app/templates',
    '--add-data', 'webapp/app/static;app/static',
    '--collect-all', 'flask',
    '--collect-all', 'flask_sqlalchemy',
    '--collect-all', 'flask_login',
    '--collect-all', 'werkzeug',
    '--collect-all', 'sqlalchemy',
    '--collect-all', 'webview',
    '--collect-all', 'PIL',
    '--noconfirm', '--clean',
    'launcher.py'
]

print("Command:", ' '.join(cmd))
result = subprocess.run(cmd)
if result.returncode != 0:
    print("Build failed!")
    sys.exit(1)

exe_path = os.path.join(SCRIPT_DIR, 'dist', 'Jesus Projekt Erfurt.exe')
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\nBuild successful! Size: {size_mb:.1f} MB")
    print(f"Executable: {exe_path}")
else:
    print("Build failed - executable not found")
    sys.exit(1)
