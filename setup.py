#!/usr/bin/env python3
"""
Campus Recruitment System Setup Script
Run this in VS Code terminal to set up your environment
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "="*60)
    print(f"🚀 {text}")
    print("="*60)

def print_step(step, text):
    print(f"\n✅ Step {step}: {text}")

def run_command(cmd, description=""):
    """Run a command and return success status"""
    try:
        if description:
            print(f"   {description}...")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Success")
            return True
        else:
            print(f"   ❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print_header("Campus Recruitment System Setup")
    
    print(f"🖥️  Platform: {platform.system()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print("   ✅ Python version is compatible")
    
    # Step 2: Create directories
    print_step(2, "Creating Required Directories")
    directories = [
        'campus/uploads',
        'dashboard/uploads',
        '.vscode'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ Created: {directory}")
        except Exception as e:
            print(f"   ❌ Failed to create {directory}: {e}")
    
    # Step 3: Install dependencies
    print_step(3, "Installing Python Dependencies")
    dependencies = [
        'Flask==2.3.3',
        'Flask-CORS==4.0.0', 
        'pandas==2.1.4',
        'requests==2.31.0',
        'Werkzeug==2.3.7',
        'openpyxl==3.1.2',
        'numpy==1.24.4'
    ]
    
    for dep in dependencies:
        if not run_command(f'pip install {dep}', f"Installing {dep}"):
            print(f"⚠️  Failed to install {dep}, but continuing...")
    
    # Step 4: Verify installation
    print_step(4, "Verifying Installation")
    test_imports = [
        'flask',
        'flask_cors', 
        'pandas',
        'requests',
        'werkzeug',
        'openpyxl',
        'numpy'
    ]
    
    failed_imports = []
    for module in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            failed_imports.append(module)
    
    # Step 5: Check file structure
    print_step(5, "Checking File Structure")
    required_files = [
        'dashboard/app.py',
        'form.py',
        'campus/recruitment-form-dynamic.html',
        'campus/login.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    # Summary
    print_header("Setup Summary")
    
    if failed_imports:
        print(f"⚠️  Failed to import: {', '.join(failed_imports)}")
        print("   Try running: pip install <package_name>")
    
    if missing_files:
        print(f"⚠️  Missing files: {', '.join(missing_files)}")
        print("   Please ensure all project files are present")
    
    if not failed_imports and not missing_files:
        print("🎉 Setup completed successfully!")
        print("\n📍 Next Steps:")
        print("1. In VS Code, press Ctrl+Shift+P")
        print("2. Type 'Tasks: Run Task'")
        print("3. Select 'Start Both Backends'")
        print("\n🌐 Access Points:")
        print("   📊 Dashboard: http://127.0.0.1:5000")
        print("   📝 Form: http://127.0.0.1:5001")
    else:
        print("⚠️  Setup completed with warnings. Please check the issues above.")
    
    return len(failed_imports) == 0 and len(missing_files) == 0

if __name__ == '__main__':
    success = main()
    
    if platform.system().lower() == 'windows':
        input("\nPress Enter to exit...")
    
    sys.exit(0 if success else 1)