"""Build script for creating the .exe - pure tkinter, no browser, no webview"""
import os
import sys
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("Jesus Projekt Erfurt - Build Script (Pure Tkinter)")
print("=" * 60)
print(f"Build: {SCRIPT_DIR}")

# Clean previous build
for item in ['dist', 'build']:
    path = os.path.join(SCRIPT_DIR, item)
    if os.path.exists(path):
        print(f"Cleaning {path}...")
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"  Warning: {e}")
for spec_file in ['app.spec', 'launcher.spec']:
    path = os.path.join(SCRIPT_DIR, spec_file)
    if os.path.exists(path):
        os.remove(path)

# Build with PyInstaller
print("\nBuilding .exe...")
os.chdir(SCRIPT_DIR)

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile', '--windowed',
    '--name', 'Jesus Projekt Erfurt',
    '--icon', 'app.ico',
    '--add-data', 'app.ico;.',
    '--add-data', 'logo.jpg;.',
    '--collect-all', 'tkinter',
    '--collect-all', 'PIL',
    '--noconfirm', '--clean',
    'launcher.py'
]
print("Command:", ' '.join(cmd))
result = subprocess.run(cmd)
if result.returncode != 0:
    print("Build failed!")
    sys.exit(1)

# Copy update.bat and README to dist folder
import shutil
dist_dir = os.path.join(SCRIPT_DIR, 'dist')
for extra_file in ['update.bat', 'README.md']:
    src = os.path.join(SCRIPT_DIR, extra_file)
    dst = os.path.join(dist_dir, extra_file)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {extra_file} to dist/")

exe_path = os.path.join(SCRIPT_DIR, 'dist', 'Jesus Projekt Erfurt.exe')
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\nBuild successful! Size: {size_mb:.1f} MB")
    print(f"Executable: {exe_path}")
else:
    print("Build failed - executable not found")
    sys.exit(1)
