"""Build script for creating the .exe"""
import os
import sys
import shutil
import subprocess

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("Jesus Projekt Erfurt - Build Script")
print("=" * 60)
print(f"Build directory: {SCRIPT_DIR}")

# Clean previous build
for item in ['dist', 'build']:
    path = os.path.join(SCRIPT_DIR, item)
    if os.path.exists(path):
        print(f"Cleaning {path}...")
        shutil.rmtree(path)

for spec_file in ['app.spec']:
    path = os.path.join(SCRIPT_DIR, spec_file)
    if os.path.exists(path):
        os.remove(path)

# Build with PyInstaller
print("\nBuilding .exe with PyInstaller...")
os.chdir(SCRIPT_DIR)

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--windowed',
    '--name', 'Jesus Projekt Erfurt',
    '--icon', 'app.ico',
    '--collect-all', 'PIL',
    '--noconfirm',
    '--clean',
    'app.py'
]

print("Command:", ' '.join(cmd))
result = subprocess.run(cmd)
if result.returncode != 0:
    print("Build failed!")
    sys.exit(1)

# Verify
exe_path = os.path.join(SCRIPT_DIR, 'dist', 'Jesus Projekt Erfurt.exe')
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\nBuild successful!")
    print(f"Executable: {exe_path}")
    print(f"Size: {size_mb:.1f} MB")
else:
    print("Build failed - executable not found")
    sys.exit(1)
