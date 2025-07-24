# 🚀 Campus Recruitment System - VS Code Setup Guide

## 📋 **Prerequisites**

1. **VS Code** installed on your laptop
2. **Python 3.8+** installed and added to PATH
3. **Python Extension** for VS Code installed

---

## 🛠️ **Step-by-Step Setup**

### **Step 1: Open Project in VS Code**

1. Open VS Code
2. **File** → **Open Folder**
3. Navigate to: `D:\Internship\campusrecruitment-main`
4. Click **"Select Folder"**

### **Step 2: Set Up Python Environment**

1. **Open Terminal in VS Code:**
   - Press `Ctrl + `` (backtick)
   - Or **View** → **Terminal**

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment:**
   ```bash
   venv\Scripts\activate
   ```
   You should see `(venv)` at the beginning of your terminal prompt.

4. **Run Setup Script:**
   ```bash
   python setup.py
   ```
   This will install all dependencies and verify your setup.

### **Step 3: Configure Python Interpreter**

1. Press `Ctrl + Shift + P`
2. Type: **"Python: Select Interpreter"**
3. Choose: `.\venv\Scripts\python.exe`

---

## 🚀 **Running the Application**

### **Method 1: Using VS Code Tasks (Recommended)**

1. Press `Ctrl + Shift + P`
2. Type: **"Tasks: Run Task"**
3. Select: **"Start Both Backends"**

This will open two terminal tabs running both backends simultaneously.

### **Method 2: Using Debug Configuration**

1. Go to **Run and Debug** panel (`Ctrl + Shift + D`)
2. Select: **"Start Both Backends"** from dropdown
3. Press **F5** or click the play button

### **Method 3: Manual Terminal Commands**

**Terminal 1 - Dashboard Backend:**
```bash
venv\Scripts\activate
cd dashboard
python app.py
```

**Terminal 2 - Form Backend:**
```bash
venv\Scripts\activate
python form.py
```

---

## 🌐 **Access Points**

Once both backends are running:

- **📊 Admin Dashboard:** http://127.0.0.1:5000
  - Username: `admin`
  - Password: `admin123`

- **📝 Application Form:** http://127.0.0.1:5001

- **🔐 Login Page:** http://127.0.0.1:5001/login.html

---

## 🔧 **VS Code Features Available**

### **1. Debugging**
- Set breakpoints in Python code
- Step through code execution
- Inspect variables and call stack

### **2. IntelliSense**
- Auto-completion for Python code
- Syntax highlighting
- Error detection

### **3. Integrated Terminal**
- Multiple terminal tabs
- Environment activation
- Command history

### **4. File Explorer**
- Quick navigation between files
- Search across project
- Git integration

---

## 📁 **Project Structure in VS Code**

```
campusrecruitment-main/
├── .vscode/                    # VS Code configuration
│   ├── launch.json            # Debug configurations
│   ├── tasks.json             # Task definitions
│   └── settings.json          # Workspace settings
├── dashboard/                  # Dashboard backend
│   ├── app.py                 # Main dashboard app
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, JS, images
│   └── uploads/               # Uploaded files
├── campus/                     # Form frontend
│   ├── recruitment-form-dynamic.html
│   ├── login.html
│   └── uploads/               # Form uploads
├── venv/                      # Virtual environment
├── form.py                    # Form backend
├── setup.py                   # Setup script
└── requirements.txt           # Dependencies
```

---

## 🛠️ **Available VS Code Tasks**

Press `Ctrl + Shift + P` → "Tasks: Run Task" → Select:

1. **Setup Environment** - Install all dependencies
2. **Start Dashboard** - Run dashboard backend only
3. **Start Form Backend** - Run form backend only
4. **Start Both Backends** - Run both simultaneously
5. **Create Directories** - Create required folders

---

## 🐛 **Debugging in VS Code**

### **To Debug Dashboard Backend:**
1. Open `dashboard/app.py`
2. Set breakpoints by clicking left of line numbers
3. Press `F5` → Select "Dashboard Backend"
4. Access http://127.0.0.1:5000 to trigger breakpoints

### **To Debug Form Backend:**
1. Open `form.py`
2. Set breakpoints
3. Press `F5` → Select "Form Backend"
4. Submit a form to trigger breakpoints

---

## 🔍 **Troubleshooting**

### **Issue: "Python not found"**
**Solution:**
1. Install Python from python.org
2. Ensure "Add to PATH" was checked during installation
3. Restart VS Code

### **Issue: "Module not found"**
**Solution:**
1. Ensure virtual environment is activated: `venv\Scripts\activate`
2. Run: `python setup.py`
3. Or manually: `pip install -r requirements.txt`

### **Issue: "Port already in use"**
**Solution:**
1. In VS Code terminal: `netstat -ano | findstr :5000`
2. Kill process: `taskkill /PID <PID> /F`
3. Repeat for port 5001

### **Issue: "Virtual environment not found"**
**Solution:**
1. Delete `venv` folder
2. Run: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Run: `python setup.py`

---

## 💡 **VS Code Tips**

1. **Quick File Navigation:** `Ctrl + P` → Type filename
2. **Search in Files:** `Ctrl + Shift + F`
3. **Multi-cursor:** `Alt + Click`
4. **Terminal Split:** Click split icon in terminal
5. **Zen Mode:** `Ctrl + K, Z` for distraction-free coding

---

## 🔄 **Daily Workflow**

### **Starting Work:**
1. Open VS Code
2. Open project folder
3. `Ctrl + Shift + P` → "Tasks: Run Task" → "Start Both Backends"
4. Access http://127.0.0.1:5000

### **During Development:**
1. Edit files in VS Code
2. Save changes (`Ctrl + S`)
3. Flask auto-reloads (you'll see restart messages in terminal)
4. Refresh browser to see changes

### **Stopping Work:**
1. In terminal tabs, press `Ctrl + C` to stop servers
2. Close VS Code

---

## 🎯 **What You Get**

✅ **Professional Development Environment**
- Syntax highlighting and IntelliSense
- Integrated debugging with breakpoints
- Git integration for version control
- Multiple terminal support

✅ **Easy Project Management**
- One-click setup and startup
- Organized file structure
- Quick navigation between components

✅ **Debugging Capabilities**
- Step through code execution
- Inspect variables and database queries
- Set conditional breakpoints

✅ **Modern UI & Full Functionality**
- Beautiful dashboard with glass-morphism design
- Fully functional application form
- Real-time data updates
- Comprehensive error handling

---

## 🎉 **You're Ready!**

Your VS Code environment is now perfectly configured for the Campus Recruitment System. You have:

- ✅ Professional development setup
- ✅ One-click startup and debugging
- ✅ Beautiful, modern UI
- ✅ Fully functional form and dashboard
- ✅ Comprehensive error handling

**Happy Coding! 💻✨**