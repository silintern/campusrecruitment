#!/usr/bin/env python3
"""
Development Runner for Campus Recruitment System
Run this script to start both backends simultaneously
"""

import os
import sys
import time
import threading
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    print("\n" + "="*60)
    print("🚀 Campus Recruitment System - Development Server")
    print("="*60)
    print("Starting both backends...")
    print()

def run_dashboard():
    """Run the dashboard backend"""
    print("📊 Starting Dashboard Backend on port 5000...")
    
    # Change to dashboard directory
    dashboard_dir = Path(__file__).parent / "dashboard"
    os.chdir(dashboard_dir)
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n📊 Dashboard Backend stopped.")
    except Exception as e:
        print(f"❌ Dashboard Backend error: {e}")
    finally:
        # Change back to project root
        os.chdir(Path(__file__).parent)

def run_form():
    """Run the form backend"""
    print("📝 Starting Form Backend on port 5001...")
    
    try:
        subprocess.run([sys.executable, "form.py"], check=True)
    except KeyboardInterrupt:
        print("\n📝 Form Backend stopped.")
    except Exception as e:
        print(f"❌ Form Backend error: {e}")

def main():
    print_banner()
    
    # Check if we're in the right directory
    if not (Path("dashboard/app.py").exists() and Path("form.py").exists()):
        print("❌ Error: Required files not found!")
        print("Please run this script from the project root directory.")
        return
    
    # Create necessary directories
    Path("campus/uploads").mkdir(parents=True, exist_ok=True)
    Path("dashboard/uploads").mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created/verified")
    print()
    
    try:
        # Start dashboard in a separate thread
        dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        dashboard_thread.start()
        
        # Wait a moment for dashboard to start
        time.sleep(3)
        
        # Start form backend in main thread
        run_form()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all servers...")
        print("✅ Campus Recruitment System stopped.")

if __name__ == '__main__':
    main()