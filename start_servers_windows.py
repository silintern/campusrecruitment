#!/usr/bin/env python3
"""
Windows-compatible startup script for Campus Recruitment System
"""

import subprocess
import time
import sys
import os
import platform
from threading import Thread

def is_windows():
    return platform.system().lower() == 'windows'

def get_python_executable():
    """Get the correct Python executable path"""
    if is_windows():
        # Check if we're in a virtual environment
        if os.path.exists('venv/Scripts/python.exe'):
            return 'venv/Scripts/python.exe'
        elif os.path.exists('venv/Scripts/python3.exe'):
            return 'venv/Scripts/python3.exe'
    
    # Fallback to system Python
    return sys.executable

def run_dashboard():
    """Run the dashboard backend on port 5000"""
    print("🔧 Starting Dashboard Backend (Port 5000)...")
    python_exe = get_python_executable()
    
    try:
        if is_windows():
            # Change to dashboard directory
            dashboard_path = os.path.join(os.getcwd(), 'dashboard')
            subprocess.run([python_exe, 'app.py'], cwd=dashboard_path, check=True)
        else:
            os.chdir('dashboard')
            subprocess.run([python_exe, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n📊 Dashboard Backend stopped.")
    except Exception as e:
        print(f"❌ Dashboard Backend error: {e}")
        print(f"💡 Make sure you've run setup_windows.bat first!")
    finally:
        if not is_windows():
            os.chdir('..')

def run_form():
    """Run the form backend on port 5001"""
    print("📋 Starting Form Backend (Port 5001)...")
    python_exe = get_python_executable()
    
    try:
        subprocess.run([python_exe, 'form.py'], check=True)
    except KeyboardInterrupt:
        print("\n📝 Form Backend stopped.")
    except Exception as e:
        print(f"❌ Form Backend error: {e}")
        print(f"💡 Make sure you've run setup_windows.bat first!")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'pandas', 'requests', 'flask_cors']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("💡 Please run setup_windows.bat to install dependencies.")
        return False
    
    return True

def main():
    print("🚀 Starting Campus Recruitment System...")
    print("=" * 50)
    
    # Check if we're on Windows and have virtual environment
    if is_windows() and not os.path.exists('venv'):
        print("❌ Virtual environment not found!")
        print("💡 Please run setup_windows.bat first to set up the environment.")
        input("Press Enter to exit...")
        return
    
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return
    
    print(f"🖥️  Platform: {platform.system()}")
    print(f"🐍 Python: {get_python_executable()}")
    print()
    
    # Start dashboard backend in a separate thread
    dashboard_thread = Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Wait a moment for dashboard to start
    print("⏳ Waiting for dashboard to initialize...")
    time.sleep(3)
    
    # Start form backend in main thread
    try:
        run_form()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all servers...")
        print("✅ Campus Recruitment System stopped.")
        if is_windows():
            input("Press Enter to exit...")

if __name__ == '__main__':
    main()