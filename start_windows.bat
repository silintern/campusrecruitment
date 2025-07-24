@echo off
echo.
echo ============================================================
echo 🚀 Starting Campus Recruitment System
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo.
    echo Please run setup_windows.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment found

REM Check if required files exist
if not exist "dashboard\app.py" (
    echo ❌ Dashboard backend not found!
    echo Please ensure dashboard\app.py exists
    echo.
    pause
    exit /b 1
)

if not exist "form.py" (
    echo ❌ Form backend not found!
    echo Please ensure form.py exists
    echo.
    pause
    exit /b 1
)

echo ✅ Backend files verified

REM Kill any existing processes on ports 5000 and 5001
echo 🔄 Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5001" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo.
echo 📊 Starting Dashboard Backend (Port 5000)...
start "Campus Recruitment - Dashboard Backend" cmd /k "title Dashboard Backend (Port 5000) && venv\Scripts\activate.bat && cd dashboard && echo ✅ Dashboard Backend Starting... && python app.py"

echo ⏳ Waiting for dashboard to start...
timeout /t 5 /nobreak > nul

echo.
echo 📝 Starting Form Backend (Port 5001)...
start "Campus Recruitment - Form Backend" cmd /k "title Form Backend (Port 5001) && venv\Scripts\activate.bat && echo ✅ Form Backend Starting... && python form.py"

echo ⏳ Waiting for form backend to start...
timeout /t 3 /nobreak > nul

echo.
echo ============================================================
echo ✅ Both backends are starting in separate windows
echo ============================================================
echo.
echo 🌐 Access Points:
echo   📊 Admin Dashboard: http://127.0.0.1:5000
echo   📝 Application Form: http://127.0.0.1:5001
echo   🔐 Form Login: http://127.0.0.1:5001/login.html
echo.
echo 💡 Tips:
echo   - Both backends will open in separate command windows
echo   - Close those windows to stop the servers
echo   - Check the command windows for any error messages
echo   - If ports are busy, the setup will try to kill existing processes
echo.
echo 🔄 To restart: Run this script again
echo 🛑 To stop: Close the backend command windows
echo.
echo ============================================================

REM Wait a bit more and try to open the dashboard in browser
timeout /t 5 /nobreak > nul
echo 🌐 Opening dashboard in your default browser...
start http://127.0.0.1:5000

echo.
echo ✅ Setup complete! The dashboard should open in your browser.
echo 💡 Press any key to close this window (backends will continue running)
pause > nul