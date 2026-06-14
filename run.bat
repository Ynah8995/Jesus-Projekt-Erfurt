@echo off
echo ============================================
echo   Jesus Projekt Erfurt - Birthday Monitoring
echo ============================================
echo.

cd /d "%~dp0"

echo Opening browser in 3 seconds...
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:5001"

python run.py

pause
