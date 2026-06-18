# Jesus Projekt Erfurt - Birthday Monitoring (Desktop App)

## Standalone Desktop Application

This is a self-contained desktop application that runs without a browser.

## Features

- **No browser needed** - Native tkinter UI
- **Loading screen** - Nice progress bar on startup
- **Self-contained** - All dependencies bundled in the .exe
- **Local database** - SQLite database stored next to the .exe
- **AppData fallback** - If write permissions denied, database stored in `%APPDATA%/Jesus Projekt Erfurt/`
- **No test data** - Database starts empty, only your entered data

## Installation

1. Download `Jesus Projekt Erfurt.exe` from `desktop_app/dist/`
2. Place it in any folder
3. Run it!

## Database Location

- **Primary**: Same folder as the .exe (e.g., `C:\Users\YourName\Desktop\birthday_monitoring.db`)
- **Fallback**: `%APPDATA%\Jesus Projekt Erfurt\birthday_monitoring.db`

The app will automatically detect which location to use based on write permissions.

## First Run

1. The app creates a loading screen
2. Creates an empty database
3. Shows the login screen
4. **No default users** - You need to create the first user via the registration (run `python register_admin.py` first time, or use the CLI)

## Building from Source

```bash
cd desktop_app
pip install pillow pyinstaller
python -m PyInstaller --onefile --windowed --name "Jesus Projekt Erfurt" app.py
```

The .exe will be in `dist/Jesus Projekt Erfurt.exe`.

## File Structure

- `app.py` - Main entry point with loading screen
- `main_app.py` - Main application windows (Login, Dashboard, Clients, Users, Settings)
- `models.py` - Database models
- `build.py` - Build script for PyInstaller
