@echo off
title Jesus Projekt Erfurt - Update Tool
echo ============================================
echo   Jesus Projekt Erfurt - Update Tool
echo ============================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if the exe is running
tasklist /FI "IMAGENAME eq Jesus Projekt Erfurt.exe" 2>NUL | find /I /N "Jesus Projekt Erfurt.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [!] The application is currently running.
    echo     Please close it before updating.
    echo.
    pause
    exit /b 1
)

REM Check if both old and new exe exist
if not exist "Jesus Projekt Erfurt.exe" (
    echo [X] ERROR: Jesus Projekt Erfurt.exe not found in this folder.
    echo     Place this update.bat in the same folder as the existing app.
    echo.
    pause
    exit /b 1
)

if not exist "Jesus Projekt Erfurt.exe.new" (
    echo [X] ERROR: Jesus Projekt Erfurt.exe.new not found.
    echo.
    echo To update:
    echo   1. Download the new version
    echo   2. Rename it to "Jesus Projekt Erfurt.exe.new"
    echo   3. Place it in the same folder as this update.bat
    echo   4. Run this update.bat again
    echo.
    pause
    exit /b 1
)

echo [1/4] Backing up current version...
if exist "Jesus Projekt Erfurt.exe.bak" del "Jesus Projekt Erfurt.exe.bak"
copy /Y "Jesus Projekt Erfurt.exe" "Jesus Projekt Erfurt.exe.bak" >NUL
if errorlevel 1 (
    echo [X] ERROR: Failed to create backup.
    pause
    exit /b 1
)
echo     [OK] Backup saved as Jesus Projekt Erfurt.exe.bak

echo.
echo [2/4] Verifying data files are safe...
if exist "birthday_monitoring.db" (
    echo     [OK] Database found: birthday_monitoring.db
) else (
    echo     [i] No database found (will be created on first run)
)

if exist "preferences.json" (
    echo     [OK] Preferences found: preferences.json
)

if exist "uploads" (
    echo     [OK] Uploads folder found
)
echo     All data files will be PRESERVED.

echo.
echo [3/4] Installing new version...
del "Jesus Projekt Erfurt.exe" >NUL 2>&1
if exist "Jesus Projekt Erfurt.exe" (
    echo [X] ERROR: Could not delete old file. It may be in use.
    echo     Please close any program using it and try again.
    pause
    exit /b 1
)
move /Y "Jesus Projekt Erfurt.exe.new" "Jesus Projekt Erfurt.exe" >NUL
if errorlevel 1 (
    echo [X] ERROR: Failed to install new version.
    echo     Restoring backup...
    move /Y "Jesus Projekt Erfurt.exe.bak" "Jesus Projekt Erfurt.exe" >NUL
    pause
    exit /b 1
)
echo     [OK] New version installed successfully!

echo.
echo [4/4] Cleanup...
echo     [OK] Update complete!

echo.
echo ============================================
echo   Update Successful!
echo ============================================
echo.
echo Your data has been preserved:
if exist "birthday_monitoring.db" echo   - Database: birthday_monitoring.db
if exist "preferences.json" echo   - Preferences: preferences.json
if exist "uploads" echo   - Uploads: uploads/ folder
echo   - Backup of old version: Jesus Projekt Erfurt.exe.bak
echo.
echo You can now run the updated application.
echo.
pause
