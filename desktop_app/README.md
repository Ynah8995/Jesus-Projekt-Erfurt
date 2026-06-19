# Jesus Projekt Erfurt - Birthday Monitoring (Desktop App)

## What is this?

A self-contained Windows desktop application for monitoring client birthdays. Built with Python + tkinter, packaged as a single `.exe` file that requires no installation.

---

## How to deploy (give the .exe to someone)

### Step 1: Copy the file
Copy `Jesus Projekt Erfurt.exe` to any folder on the user's computer. For example:
- `C:\Program Files\Jesus Projekt Erfurt\`
- `C:\Users\Username\Desktop\Jesus Projekt Erfurt\`
- `D:\Apps\Birthday Monitoring\`

**That's it!** The app is fully self-contained. No installation, no Python, no browser, no dependencies.

### Step 2: First run
When the user runs the .exe for the first time:
1. A loading screen appears with the Jesus Projekt Erfurt logo
2. A database file (`birthday_monitoring.db`) is automatically created in the same folder
3. A default admin account is created:
   - **Username:** `admin`
   - **Password:** `admin123`
4. The login screen appears

### Step 3: Change the default password
The user should immediately:
1. Log in with `admin` / `admin123`
2. Go to the user menu (top right) → **Edit Profile**
3. Change the username and password
4. Add other users via **Users** → **Add User**

---

## Where is the data stored?

| File | Location | Purpose |
|------|----------|---------|
| `birthday_monitoring.db` | Same folder as `.exe` | All data (users, clients, settings) |
| `preferences.json` | Same folder as `.exe` | Language preference, last username |
| `uploads/` | Same folder as `.exe` | Profile pictures |
| `logo.jpg` | Same folder as `.exe` | App logo (downloaded on first run) |

**If the user can't write to the folder** (e.g., `Program Files`), the data is stored in:
`%APPDATA%\Jesus Projekt Erfurt\`

---

## How to update without losing data

### Method 1: Manual replacement (simplest)

1. **Close the app** if it's running
2. **Back up** the current `.exe` (just in case)
3. **Copy the new `.exe`** over the old one (replace the file)
4. **Run the new `.exe`** - the database and all data are preserved

**That's it!** The new version reads the existing database. No data loss.

### Method 2: Using the update script

Use the included `update.bat` script:
1. Place the new `Jesus Projekt Erfurt.exe` in the same folder as `update.bat`
2. Double-click `update.bat`
3. It will:
   - Stop the running app (if any)
   - Back up the old `.exe` as `Jesus Projekt Erfurt.exe.bak`
   - Replace with the new version
   - Keep all data files (database, uploads, preferences) intact

### Method 3: Using the built-in updater (future feature)

A future version will include a built-in updater that checks for updates from GitHub.

---

## File structure after deployment

```
📁 Jesus Projekt Erfurt/
├── 🎂 Jesus Projekt Erfurt.exe      ← The application
├── 💾 birthday_monitoring.db         ← Database (auto-created)
├── ⚙️ preferences.json               ← User preferences (auto-created)
├── 📁 uploads/                       ← Profile pictures (auto-created)
│   └── 🖼️ user_1_abc12345.jpg
├── 🖼️ logo.jpg                        ← App logo (auto-downloaded)
└── 🔄 update.bat                     ← Optional: update helper script
```

---

## Default login credentials

- **Username:** `admin`
- **Password:** `admin123`

**⚠️ Change these immediately after first login!**

---

## System requirements

- **OS:** Windows 10 or Windows 11
- **RAM:** 100 MB minimum
- **Disk:** 50 MB for the app + space for data
- **Internet:** Only needed for:
  - First run (downloads the logo)
  - Sending birthday email greetings
  - Future updates from GitHub

---

## Troubleshooting

### App doesn't start
- Make sure Windows 10/11 (64-bit)
- Try running as Administrator
- Check if antivirus is blocking it
- Delete `preferences.json` and try again

### Database errors
- Make sure the folder is writable
- Or let the app use `%APPDATA%\Jesus Projekt Erfurt\`
- Delete `birthday_monitoring.db` to reset (WARNING: loses all data)

### Forgot admin password
- Delete `birthday_monitoring.db` to reset (loses all data)
- Or modify the database directly using a SQLite browser

### Want to start fresh
- Close the app
- Delete `birthday_monitoring.db`, `preferences.json`, and `uploads/` folder
- Run the app again

---

## Features

- 👤 User management (admin/staff roles)
- 🎂 Client birthday tracking by month
- 📧 Send birthday greetings via email
- 🌐 Bilingual (English/German)
- 📷 Profile picture upload
- 💾 Self-contained database (no server needed)
- 🎨 Modern UI with Jesus Projekt Erfurt branding
