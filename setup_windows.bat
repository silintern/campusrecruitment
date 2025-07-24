@echo off
echo.
echo ============================================================
echo 🚀 Campus Recruitment System - Windows Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version

REM Check if we're in the correct directory
if not exist "dashboard" (
    echo ❌ Error: dashboard folder not found
    echo Please run this script from the project root directory
    echo.
    pause
    exit /b 1
)

if not exist "campus" (
    echo ❌ Error: campus folder not found
    echo Please run this script from the project root directory
    echo.
    pause
    exit /b 1
)

echo ✅ Project structure verified

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        echo.
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo 📥 Installing dependencies...

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    echo.
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing Flask and dependencies...
pip install Flask==2.3.3
if errorlevel 1 (
    echo ❌ Failed to install Flask
    pause
    exit /b 1
)

pip install Flask-CORS==4.0.0
if errorlevel 1 (
    echo ❌ Failed to install Flask-CORS
    pause
    exit /b 1
)

pip install pandas==2.1.4
if errorlevel 1 (
    echo ❌ Failed to install pandas
    pause
    exit /b 1
)

pip install requests==2.31.0
if errorlevel 1 (
    echo ❌ Failed to install requests
    pause
    exit /b 1
)

pip install Werkzeug==2.3.7
if errorlevel 1 (
    echo ❌ Failed to install Werkzeug
    pause
    exit /b 1
)

pip install openpyxl==3.1.2
if errorlevel 1 (
    echo ❌ Failed to install openpyxl
    pause
    exit /b 1
)

pip install numpy==1.24.4
if errorlevel 1 (
    echo ❌ Failed to install numpy
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies installed successfully!

REM Create uploads directory
if not exist "campus\uploads" (
    mkdir "campus\uploads"
    echo ✅ Created uploads directory
)

REM Create dashboard uploads directory
if not exist "dashboard\uploads" (
    mkdir "dashboard\uploads"
    echo ✅ Created dashboard uploads directory
)

echo.
echo ============================================================
echo ✅ Setup completed successfully!
echo ============================================================
echo.
echo 🎯 Next steps:
echo 1. Run: start_windows.bat
echo    OR
echo 2. Manual start:
echo    - Dashboard: cd dashboard ^&^& python app.py
echo    - Form: python form.py
echo.
echo 🌐 Access Points:
echo   📊 Admin Dashboard: http://127.0.0.1:5000
echo   📝 Application Form: http://127.0.0.1:5001
echo   🔐 Form Login: http://127.0.0.1:5001/login.html
echo.
echo ============================================================
pause