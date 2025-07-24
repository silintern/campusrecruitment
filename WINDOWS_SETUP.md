# Windows Setup Guide for Campus Recruitment System

## 🚀 Quick Setup (Recommended)

### Step 1: Run the Setup Script
```batch
# Double-click or run in Command Prompt:
setup_windows.bat
```

This will:
- ✅ Create a virtual environment
- ✅ Install all required Python packages
- ✅ Set up the project dependencies

### Step 2: Start the System
```batch
# Double-click or run in Command Prompt:
start_windows.bat
```

This will open two separate command windows:
- 📊 **Dashboard Backend** (Port 5000)
- 📝 **Form Backend** (Port 5001)

## 🌐 Access Points

- **📊 Admin Dashboard:** http://127.0.0.1:5000
- **📝 Application Form:** http://127.0.0.1:5001
- **🔐 Form Login:** http://127.0.0.1:5001/login.html

## 🔧 Manual Setup (If Automatic Setup Fails)

### Prerequisites
1. **Python 3.8+** installed and added to PATH
2. **pip** package manager

### Step-by-Step Manual Installation

1. **Open Command Prompt as Administrator**

2. **Navigate to project directory:**
```cmd
cd "D:\Internship\campusrecruitment-main"
```

3. **Create virtual environment:**
```cmd
python -m venv venv
```

4. **Activate virtual environment:**
```cmd
venv\Scripts\activate.bat
```

5. **Upgrade pip:**
```cmd
python -m pip install --upgrade pip
```

6. **Install required packages:**
```cmd
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install pandas==2.1.4
pip install requests==2.31.0
pip install Werkzeug==2.3.7
pip install openpyxl==3.1.2
pip install numpy==1.24.4
```

7. **Start the backends:**

**Terminal 1 - Dashboard:**
```cmd
venv\Scripts\activate.bat
cd dashboard
python app.py
```

**Terminal 2 - Form:**
```cmd
venv\Scripts\activate.bat
python form.py
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. "ModuleNotFoundError: No module named 'pandas'"
**Solution:**
```cmd
venv\Scripts\activate.bat
pip install pandas==2.1.4
```

#### 2. "Virtual environment not found"
**Solution:**
```cmd
# Delete existing venv folder if corrupted
rmdir /s venv
# Run setup again
setup_windows.bat
```

#### 3. "Python is not recognized"
**Solutions:**
- Install Python from https://python.org
- During installation, check "Add Python to PATH"
- Or manually add Python to Windows PATH

#### 4. "Permission denied" errors
**Solutions:**
- Run Command Prompt as Administrator
- Check antivirus software isn't blocking Python
- Ensure you have write permissions to the directory

#### 5. Port already in use
**Solution:**
```cmd
# Find processes using ports 5000 and 5001
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# Kill the processes (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### 6. Flask import errors
**Solution:**
```cmd
venv\Scripts\activate.bat
pip uninstall Flask
pip install Flask==2.3.3
```

## 🔄 Alternative Startup Methods

### Method 1: Batch Files (Recommended)
```batch
setup_windows.bat    # One-time setup
start_windows.bat     # Start both backends
```

### Method 2: Python Script
```cmd
venv\Scripts\activate.bat
python start_servers_windows.py
```

### Method 3: Manual (Two terminals)
**Terminal 1:**
```cmd
venv\Scripts\activate.bat
cd dashboard
python app.py
```

**Terminal 2:**
```cmd
venv\Scripts\activate.bat
python form.py
```

## 📁 Directory Structure After Setup

```
campusrecruitment-main/
├── venv/                          # Virtual environment
│   ├── Scripts/
│   │   ├── activate.bat          # Activation script
│   │   └── python.exe            # Python executable
│   └── Lib/                      # Installed packages
├── dashboard/
│   ├── app.py                    # Dashboard backend
│   └── recruitment_final.db     # Database
├── campus/
│   ├── recruitment-form-dynamic.html
│   └── uploads/                  # File uploads
├── form.py                       # Form backend
├── requirements.txt              # Python dependencies
├── setup_windows.bat            # Setup script
├── start_windows.bat            # Startup script
└── WINDOWS_SETUP.md             # This guide
```

## 🎯 Verification Steps

After setup, verify everything works:

1. **Check virtual environment:**
```cmd
venv\Scripts\activate.bat
python --version
pip list
```

2. **Test dashboard backend:**
```cmd
cd dashboard
python app.py
# Should show: Running on http://127.0.0.1:5000
```

3. **Test form backend:**
```cmd
python form.py
# Should show: Running on http://127.0.0.1:5001
```

4. **Test in browser:**
- Visit http://127.0.0.1:5000 (Dashboard)
- Visit http://127.0.0.1:5001 (Form)

## 💡 Tips for Windows Users

1. **Use Windows Terminal** or **PowerShell** for better experience
2. **Run as Administrator** if you encounter permission issues
3. **Disable antivirus temporarily** during setup if needed
4. **Use full paths** if relative paths don't work
5. **Check Windows Firewall** if ports are blocked

## 🔒 Security Notes

- The system runs on localhost (127.0.0.1) only
- No external network access by default
- Virtual environment isolates dependencies
- File uploads are restricted to PDF format only

## 📞 Support

If you continue having issues:

1. **Check Python installation:**
```cmd
python --version
pip --version
```

2. **Verify project structure** matches the directory tree above

3. **Check error messages** in the command prompt output

4. **Try the manual setup** if automatic setup fails

---

**Happy Recruiting on Windows! 🎓✨**