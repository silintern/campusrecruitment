#!/usr/bin/env python3
"""
Separate Flask backend for the Campus Recruitment Form
Runs on port 5001 and handles form submissions
"""

import os
import sqlite3
import traceback
from datetime import datetime
from collections import defaultdict
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__, 
           template_folder='campus',
           static_folder='campus/static')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'campus/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_conn():
    """Connect to the main dashboard database"""
    conn = sqlite3.connect('dashboard/recruitment_final.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_form_config_from_dashboard():
    """Fetch form configuration from the dashboard backend"""
    import requests
    try:
        response = requests.get('http://127.0.0.1:5000/api/public/form-config')
        if response.ok:
            return response.json()
        else:
            print(f"Error fetching form config: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error connecting to dashboard backend: {e}")
        # Fallback: get directly from database
        return get_form_config_from_db()

def get_form_config_from_db():
    """Fallback: Get form configuration directly from database"""
    conn = get_db_conn()
    try:
        # Get section order from form_sections table if it exists
        section_order = {}
        try:
            sections_query = conn.execute("SELECT name, section_order FROM form_sections ORDER BY section_order ASC").fetchall()
            section_order = {row['name']: row['section_order'] for row in sections_query}
        except:
            pass  # Table doesn't exist yet
        
        fields_query = conn.execute("SELECT * FROM form_config ORDER BY field_order ASC").fetchall()
        
        # Group fields by subsection for easier rendering
        subsections = defaultdict(list)
        for field in fields_query:
            subsections[field['subsection']].append(dict(field))
        
        # Order subsections by section_order if available, otherwise by first field's order
        if section_order:
            # Sort by section order, putting unordered sections at the end
            subsection_order = sorted(subsections.keys(), key=lambda k: section_order.get(k, 9999))
        else:
            # Fallback: maintain the order of subsections based on the first field's order in each
            subsection_order = sorted(subsections.keys(), key=lambda k: subsections[k][0]['field_order'])
        
        ordered_subsections = {k: subsections[k] for k in subsection_order}
        return ordered_subsections
        
    except Exception as e:
        print(f"Error fetching form config from database: {e}")
        return {}
    finally:
        conn.close()

@app.route('/')
def index():
    """Serve the login page"""
    return render_template('login.html')

@app.route('/login.html')
def login():
    """Serve the login page"""
    return render_template('login.html')

@app.route('/recruitment-form-dynamic.html')
def recruitment_form():
    """Serve the dynamic recruitment form"""
    return render_template('recruitment-form-dynamic.html')

@app.route('/api/public/form-config', methods=['GET'])
def get_public_form_config():
    """Public endpoint to fetch the form structure for applicants"""
    try:
        # First try to get from dashboard backend
        form_config = get_form_config_from_dashboard()
        
        # If that fails, get directly from database
        if not form_config:
            form_config = get_form_config_from_db()
        
        return jsonify(form_config)
    except Exception as e:
        print(f"Error in get_public_form_config: {e}")
        return jsonify({"error": "Unable to load form configuration"}), 500

@app.route('/api/submit_application', methods=['POST'])
def api_submit_application():
    """Handle form submission"""
    try:
        # Validate file upload
        if 'cv-resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
        
        file = request.files['cv-resume']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not (file and allowed_file(file.filename)):
            return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

        # Check file size
        if len(file.read()) > MAX_CONTENT_LENGTH:
            return jsonify({"error": "File size exceeds 5MB limit"}), 400
        
        # Reset file pointer
        file.seek(0)

        # Save file
        filename = secure_filename(file.filename)
        email = request.form.get('email', 'unknown')
        unique_filename = f"{secure_filename(email)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        # Prepare application data
        application_data = {
            'cv_resume_path': file_path,
            'submission_date': datetime.now().isoformat()
        }
        
        # Add all form fields
        for key, value in request.form.items():
            if key != 'cv-resume':  # Skip file field
                application_data[key] = value

        # Submit to dashboard backend
        import requests
        try:
            dashboard_response = requests.post(
                'http://127.0.0.1:5000/api/submit_application',
                files={'cv-resume': open(file_path, 'rb')},
                data=request.form
            )
            
            if dashboard_response.ok:
                return jsonify({"success": True, "message": "Application submitted successfully!"})
            else:
                error_data = dashboard_response.json() if dashboard_response.headers.get('content-type') == 'application/json' else {}
                return jsonify({"error": error_data.get("error", "Failed to submit application")}), dashboard_response.status_code
                
        except Exception as e:
            print(f"Error submitting to dashboard backend: {e}")
            # Fallback: save directly to database
            return save_application_to_db(application_data)

    except Exception as e:
        print(f"Error in api_submit_application: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "An error occurred while processing your application"}), 500

def save_application_to_db(application_data):
    """Fallback: Save application directly to database"""
    conn = get_db_conn()
    try:
        # Get form configuration to build dynamic insert
        form_config = get_form_config_from_db()
        
        # Build column names and values
        columns = ['submission_date']
        values = [application_data.get('submission_date')]
        placeholders = ['?']
        
        # Add form fields
        for section_fields in form_config.values():
            for field in section_fields:
                field_name = field['name']
                if field_name in application_data:
                    columns.append(field_name)
                    values.append(application_data[field_name])
                    placeholders.append('?')
        
        # Add resume path
        if 'cv_resume_path' in application_data:
            columns.append('resume_path')
            values.append(application_data['cv_resume_path'])
            placeholders.append('?')
        
        # Insert into database
        query = f"INSERT INTO applications ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        conn.execute(query, values)
        conn.commit()
        
        return jsonify({"success": True, "message": "Application submitted successfully!"})
        
    except Exception as e:
        print(f"Error saving to database: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Failed to save application"}), 500
    finally:
        conn.close()

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('campus/static', filename)

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """Serve uploaded files (for admin access)"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 5MB."}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Campus Recruitment Form Server Starting...")
    print("📋 Form available at: http://127.0.0.1:5001")
    print("🔗 Connected to dashboard at: http://127.0.0.1:5000")
    print("📁 Upload folder: " + os.path.abspath(UPLOAD_FOLDER))
    
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True,
        threaded=True
    )