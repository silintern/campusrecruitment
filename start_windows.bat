@echo off
echo 🚀 Starting Campus Recruitment System...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup_windows.bat first.
    pause
    exit /b 1
)

echo 📊 Starting Dashboard Backend (Port 5000)...
start "Dashboard Backend" cmd /k "venv\Scripts\activate.bat && cd dashboard && python app.py"

echo ⏳ Waiting for dashboard to start...
timeout /t 3 /nobreak > nul

echo 📝 Starting Form Backend (Port 5001)...
start "Form Backend" cmd /k "venv\Scripts\activate.bat && python form.py"

echo.
echo ✅ Both backends are starting...
echo.
echo 🌐 Access Points:
echo   📊 Admin Dashboard: http://127.0.0.1:5000
echo   📝 Application Form: http://127.0.0.1:5001
echo   🔐 Form Login: http://127.0.0.1:5001/login.html
echo.
echo 💡 Press any key to close this window (backends will continue running)
pause > nul