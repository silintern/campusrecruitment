#!/usr/bin/env python3
"""
Startup script to run both Dashboard and Form backends simultaneously
"""

import subprocess
import time
import sys
import os
from threading import Thread

def run_dashboard():
    """Run the dashboard backend on port 5000"""
    print("🔧 Starting Dashboard Backend (Port 5000)...")
    os.chdir('dashboard')
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n📊 Dashboard Backend stopped.")
    except Exception as e:
        print(f"❌ Dashboard Backend error: {e}")
    finally:
        os.chdir('..')

def run_form():
    """Run the form backend on port 5001"""
    print("📋 Starting Form Backend (Port 5001)...")
    try:
        subprocess.run([sys.executable, 'form.py'], check=True)
    except KeyboardInterrupt:
        print("\n📝 Form Backend stopped.")
    except Exception as e:
        print(f"❌ Form Backend error: {e}")

def main():
    print("🚀 Starting Campus Recruitment System...")
    print("=" * 50)
    
    # Start dashboard backend in a separate thread
    dashboard_thread = Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Wait a moment for dashboard to start
    time.sleep(2)
    
    # Start form backend in main thread
    try:
        run_form()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all servers...")
        print("✅ Campus Recruitment System stopped.")

if __name__ == '__main__':
    main()