#!/usr/bin/env python3
"""
Windows-Compatible Flask Backend for Campus Recruitment Form
Runs on port 5001 and handles form submissions with proper error handling
"""

import os
import sys
import sqlite3
import traceback
import platform
import requests
from datetime import datetime
from collections import defaultdict
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Windows path handling
def get_windows_path(path):
    """Convert path to Windows-compatible format"""
    if platform.system().lower() == 'windows':
        return path.replace('/', '\\')
    return path

# Initialize Flask app
app = Flask(__name__, 
           template_folder='campus',
           static_folder='campus')
CORS(app)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'campus', 'uploads')
DASHBOARD_DB_PATH = os.path.join(BASE_DIR, 'dashboard', 'recruitment_final.db')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = 'campus-recruitment-2024'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DASHBOARD_DB_PATH), exist_ok=True)

print(f"🚀 Form Backend Starting...")
print(f"📁 Base Directory: {BASE_DIR}")
print(f"📁 Upload Folder: {UPLOAD_FOLDER}")
print(f"📁 Database Path: {DASHBOARD_DB_PATH}")
print(f"🖥️  Platform: {platform.system()}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_conn():
    """Connect to the dashboard database with proper error handling"""
    try:
        if not os.path.exists(DASHBOARD_DB_PATH):
            print(f"⚠️  Database not found at {DASHBOARD_DB_PATH}")
            # Create basic database structure
            conn = sqlite3.connect(DASHBOARD_DB_PATH)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    position TEXT,
                    location TEXT,
                    qualification TEXT,
                    cv_resume_path TEXT,
                    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'Pending'
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS form_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    field_name TEXT NOT NULL,
                    field_type TEXT NOT NULL,
                    subsection TEXT,
                    field_order INTEGER DEFAULT 0,
                    is_required BOOLEAN DEFAULT 0,
                    options TEXT,
                    validations TEXT
                )
            ''')
            conn.commit()
            print("✅ Created basic database structure")
        else:
            conn = sqlite3.connect(DASHBOARD_DB_PATH)
            
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

def test_dashboard_connection():
    """Test connection to dashboard backend"""
    try:
        response = requests.get('http://127.0.0.1:5000/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def get_form_config_from_dashboard():
    """Fetch form configuration from dashboard backend"""
    try:
        if not test_dashboard_connection():
            print("⚠️  Dashboard backend not available, using direct database access")
            return None
            
        response = requests.get('http://127.0.0.1:5000/api/public/form-config', timeout=10)
        if response.ok:
            print("✅ Form config loaded from dashboard backend")
            return response.json()
        else:
            print(f"⚠️  Dashboard API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  Error connecting to dashboard: {e}")
        return None

def get_form_config_from_db():
    """Fallback: Get form configuration directly from database"""
    try:
        conn = get_db_conn()
        if not conn:
            return {"error": "Database connection failed"}
            
        cursor = conn.cursor()
        
        # Get form fields
        fields = cursor.execute('''
            SELECT field_name, field_type, subsection, field_order, is_required, options, validations
            FROM form_config 
            ORDER BY subsection, field_order
        ''').fetchall()
        
        # Get sections
        sections = cursor.execute('''
            SELECT DISTINCT subsection 
            FROM form_config 
            WHERE subsection IS NOT NULL AND subsection != ''
            ORDER BY MIN(field_order)
        ''').fetchall()
        
        # Organize data
        form_config = defaultdict(list)
        for field in fields:
            section = field['subsection'] or 'General Information'
            form_config[section].append({
                'field_name': field['field_name'],
                'field_type': field['field_type'],
                'field_order': field['field_order'] or 0,
                'is_required': bool(field['is_required']),
                'options': field['options'] or '',
                'validations': field['validations'] or '{}'
            })
        
        conn.close()
        print("✅ Form config loaded from database")
        return dict(form_config)
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return {"error": f"Database error: {str(e)}"}

@app.route('/')
def index():
    """Redirect to recruitment form"""
    return redirect(url_for('recruitment_form'))

@app.route('/recruitment-form-dynamic.html')
def recruitment_form():
    """Serve the recruitment form"""
    return render_template('recruitment-form-dynamic.html')

@app.route('/login.html')
def login_form():
    """Serve the login form"""
    return render_template('login.html')

@app.route('/api/public/form-config', methods=['GET'])
def get_public_form_config():
    """Public endpoint to fetch form structure"""
    try:
        print("📋 Form config requested")
        
        # Try dashboard backend first
        form_config = get_form_config_from_dashboard()
        
        # Fallback to direct database access
        if not form_config:
            form_config = get_form_config_from_db()
        
        if not form_config or 'error' in form_config:
            # Return default form structure
            default_config = {
                "Personal Information": [
                    {"field_name": "name", "field_type": "text", "is_required": True, "field_order": 1},
                    {"field_name": "email", "field_type": "email", "is_required": True, "field_order": 2},
                    {"field_name": "phone", "field_type": "tel", "is_required": True, "field_order": 3}
                ],
                "Application Details": [
                    {"field_name": "position", "field_type": "text", "is_required": True, "field_order": 4},
                    {"field_name": "location", "field_type": "text", "is_required": True, "field_order": 5},
                    {"field_name": "qualification", "field_type": "text", "is_required": True, "field_order": 6}
                ],
                "Documents": [
                    {"field_name": "cv-resume", "field_type": "file", "is_required": True, "field_order": 7}
                ]
            }
            print("✅ Using default form configuration")
            return jsonify(default_config)
        
        return jsonify(form_config)
        
    except Exception as e:
        print(f"❌ Error in get_public_form_config: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Unable to load form configuration"}), 500

@app.route('/api/submit_application', methods=['POST'])
def api_submit_application():
    """Handle form submission with comprehensive error handling"""
    try:
        print("📝 Form submission received")
        print(f"Form data keys: {list(request.form.keys())}")
        print(f"Files: {list(request.files.keys())}")
        
        # Handle file upload
        file_path = None
        if 'cv-resume' in request.files:
            file = request.files['cv-resume']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                
                try:
                    file.save(file_path)
                    print(f"✅ File saved: {file_path}")
                except Exception as e:
                    print(f"❌ File save error: {e}")
                    return jsonify({"error": "Failed to save uploaded file"}), 500
            else:
                print("⚠️  No valid file uploaded")
        
        # Prepare application data
        application_data = {}
        for key, value in request.form.items():
            if key != 'cv-resume':
                application_data[key] = value
        
        application_data['cv_resume_path'] = file_path
        application_data['submission_date'] = datetime.now().isoformat()
        application_data['status'] = 'Pending'
        
        print(f"Application data: {application_data}")
        
        # Try to submit to dashboard backend
        dashboard_success = False
        if test_dashboard_connection():
            try:
                files = {}
                if file_path and os.path.exists(file_path):
                    files['cv-resume'] = open(file_path, 'rb')
                
                dashboard_response = requests.post(
                    'http://127.0.0.1:5000/api/submit_application',
                    files=files,
                    data=request.form,
                    timeout=30
                )
                
                if files:
                    files['cv-resume'].close()
                
                if dashboard_response.ok:
                    print("✅ Application submitted to dashboard backend")
                    dashboard_success = True
                else:
                    print(f"⚠️  Dashboard submission failed: {dashboard_response.status_code}")
                    print(f"Response: {dashboard_response.text}")
                    
            except Exception as e:
                print(f"⚠️  Dashboard submission error: {e}")
        
        # Fallback: Save directly to database
        if not dashboard_success:
            print("💾 Saving directly to database...")
            result = save_application_to_db(application_data)
            if result.get('success'):
                print("✅ Application saved to database")
            else:
                print(f"❌ Database save failed: {result.get('error')}")
                return jsonify(result), 500
        
        return jsonify({
            "success": True, 
            "message": "Application submitted successfully!",
            "application_id": "APP_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        })
        
    except Exception as e:
        print(f"❌ Submission error: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "An error occurred while processing your application"}), 500

def save_application_to_db(application_data):
    """Save application directly to database"""
    try:
        conn = get_db_conn()
        if not conn:
            return {"error": "Database connection failed"}
        
        # Extract common fields
        name = application_data.get('name', '')
        email = application_data.get('email', '')
        phone = application_data.get('phone', '')
        position = application_data.get('position', '')
        location = application_data.get('location', '')
        qualification = application_data.get('qualification', '')
        cv_path = application_data.get('cv_resume_path', '')
        submission_date = application_data.get('submission_date', datetime.now().isoformat())
        status = application_data.get('status', 'Pending')
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO applications 
            (name, email, phone, position, location, qualification, cv_resume_path, submission_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, position, location, qualification, cv_path, submission_date, status))
        
        application_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"success": True, "application_id": application_id}
        
    except Exception as e:
        print(f"❌ Database save error: {e}")
        return {"error": f"Database error: {str(e)}"}

@app.route('/uploads/<filename>')
def serve_uploads(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('campus', filename)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "form-backend",
        "port": 5001,
        "platform": platform.system(),
        "database": "connected" if get_db_conn() else "disconnected",
        "dashboard_connection": "connected" if test_dashboard_connection() else "disconnected"
    })

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 10MB."}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🌐 Starting Form Backend Server...")
    print("📍 Access points:")
    print("   📝 Application Form: http://127.0.0.1:5001")
    print("   🔐 Login Form: http://127.0.0.1:5001/login.html")
    print("   ❤️  Health Check: http://127.0.0.1:5001/api/health")
    
    try:
        app.run(
            host='127.0.0.1',
            port=5001,
            debug=True,
            threaded=True,
            use_reloader=False  # Prevent double startup on Windows
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        input("Press Enter to exit...")