@echo off
echo 🚀 Setting up Campus Recruitment System for Windows...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment. Please ensure Python is installed.
        pause
        exit /b 1
    )
) else (
    echo ✅ Virtual environment already exists.
)

echo.
echo 📥 Activating virtual environment and installing dependencies...

REM Activate virtual environment and install requirements
call venv\Scripts\activate.bat

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements. Trying individual packages...
    pip install Flask==2.3.3
    pip install Flask-CORS==4.0.0
    pip install pandas==2.1.4
    pip install requests==2.31.0
    pip install Werkzeug==2.3.7
    pip install openpyxl==3.1.2
    pip install numpy==1.24.4
)

echo.
echo ✅ Setup completed successfully!
echo.
echo 🎯 To start the system:
echo 1. Run: start_windows.bat
echo    OR
echo 2. Manually:
echo    - Dashboard: cd dashboard ^&^& python app.py
echo    - Form: python form.py
echo.
pause