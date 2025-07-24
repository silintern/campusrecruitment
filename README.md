# Campus Recruitment System

A comprehensive, modern campus recruitment management system with separate backends for the admin dashboard and application form.

## 🏗️ Architecture

### Two-Backend Architecture
- **Dashboard Backend** (`dashboard/app.py`) - Port 5000
  - Admin dashboard and analytics
  - Form configuration management
  - Application data management
  - User authentication

- **Form Backend** (`form.py`) - Port 5001
  - Public recruitment form
  - Form submissions
  - File uploads
  - Communicates with dashboard backend

## 🚀 Quick Start

### Option 1: Start Both Backends Together
```bash
python3 start_servers.py
```

### Option 2: Start Backends Separately

**Terminal 1 - Dashboard Backend:**
```bash
cd dashboard
python3 app.py
```

**Terminal 2 - Form Backend:**
```bash
python3 form.py
```

## 📋 Access Points

- **📊 Admin Dashboard:** http://127.0.0.1:5000
- **📝 Application Form:** http://127.0.0.1:5001
- **🔐 Form Login:** http://127.0.0.1:5001/login.html

## ✨ Key Features

### Enhanced Admin Dashboard
- **Modern UI** with gradient backgrounds and glass-morphism effects
- **Real-time Analytics** with interactive charts
- **Advanced Form Builder** with drag-and-drop section ordering
- **Dynamic Field Management** with validation rules
- **User Management** with role-based access

### Improved Form Experience
- **Progressive Form Loading** with smooth animations
- **Real-time Progress Tracking** with completion indicators
- **Smart Validation** with instant feedback
- **Responsive Design** for all devices
- **File Upload** with drag-and-drop support

### Form Configuration System
- ✅ **Create/Edit/Delete Fields** with full validation
- ✅ **Section Management** with custom icons and descriptions
- ✅ **Drag-and-Drop Ordering** for both sections and fields
- ✅ **Dynamic Field Types** (text, email, select, radio, checkbox, file, etc.)
- ✅ **Validation Rules** (min/max length, regex patterns, custom messages)
- ✅ **Real-time Form Updates** - changes reflect immediately

## 🔧 Technical Details

### Backend Technologies
- **Flask** - Web framework
- **SQLite** - Database
- **Flask-CORS** - Cross-origin resource sharing
- **Werkzeug** - File handling and security
- **Requests** - Inter-service communication

### Frontend Technologies
- **Vanilla JavaScript** - Dynamic interactions
- **Tailwind CSS** - Styling framework
- **Chart.js** - Data visualizations
- **FontAwesome** - Icons
- **Inter Font** - Typography

### Database Schema
- `form_config` - Dynamic form field configurations
- `form_sections` - Section metadata and ordering
- `applications` - Dynamic application data
- `users` - Admin user management

## 📁 Project Structure

```
├── dashboard/                 # Admin Dashboard Backend
│   ├── app.py                # Main dashboard application
│   ├── templates/            # Dashboard HTML templates
│   ├── static/               # Dashboard assets
│   └── recruitment_final.db  # Main database
├── campus/                   # Form Frontend
│   ├── login.html           # Login page
│   ├── recruitment-form-dynamic.html  # Dynamic form
│   ├── static/              # Form assets
│   └── uploads/             # File uploads
├── form.py                  # Form Backend
├── start_servers.py         # Startup script
└── requirements-form.txt    # Form backend dependencies
```

## 🎯 Recent Improvements

### 1. Fixed Section/Field Ordering ✅
- **Backend Fix:** SQLite compatibility for section reordering
- **Frontend Fix:** Enhanced drag-and-drop with visual feedback
- **Form Integration:** Proper field ordering within sections

### 2. Enhanced Dashboard UI ✅
- **Modern Design:** Gradient backgrounds and glass-morphism
- **Better Navigation:** User menu and improved header
- **Visual Enhancements:** Card-based layouts with hover effects
- **Responsive Design:** Mobile-friendly interface

### 3. Separate Form Backend ✅
- **Dedicated Server:** Form runs on port 5001
- **Inter-service Communication:** Form backend talks to dashboard
- **Fallback Support:** Direct database access if dashboard is down
- **File Management:** Dedicated upload handling

## 🔄 Data Flow

```
User Form Submission → Form Backend (5001) → Dashboard Backend (5000) → Database
                                         ↓
                    File Upload → campus/uploads/
```

## 🛠️ Configuration

### Environment Setup
1. Install Python dependencies:
```bash
pip3 install --break-system-packages flask flask-cors pandas requests
```

2. Ensure database exists:
```bash
# Database is automatically created on first run
```

3. Create upload directories:
```bash
mkdir -p campus/uploads
mkdir -p dashboard/uploads
```

## 🔐 Security Features

- **File Upload Validation** - Only PDF files, 5MB limit
- **SQL Injection Protection** - Parameterized queries
- **CORS Configuration** - Controlled cross-origin access
- **Session Management** - Secure admin authentication
- **Input Sanitization** - All user inputs are sanitized

## 📊 Analytics & Reporting

- **Real-time KPIs** - Application counts, conversion rates
- **Interactive Charts** - Applications by company, college, etc.
- **Data Export** - CSV download with custom column selection
- **Advanced Filtering** - Date range, location, qualification filters

## 🎨 UI/UX Features

### Form Experience
- **Progress Indicators** - Real-time completion tracking
- **Smart Validation** - Instant feedback with success/error states
- **Smooth Animations** - Section entrance animations
- **Responsive Design** - Works on all screen sizes
- **Accessibility** - Keyboard navigation and screen reader support

### Dashboard Experience
- **Modern Interface** - Glass-morphism and gradient effects
- **Interactive Elements** - Hover effects and smooth transitions
- **Data Visualization** - Beautiful charts and graphs
- **Efficient Workflows** - Drag-and-drop form building

## 🚨 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find and kill process using port
lsof -ti:5000 | xargs kill -9
lsof -ti:5001 | xargs kill -9
```

**Database Connection Issues:**
- Ensure `dashboard/recruitment_final.db` exists
- Check file permissions
- Restart both backends

**Form Not Loading:**
- Verify both backends are running
- Check browser console for errors
- Ensure CORS is properly configured

## 🔄 Development Workflow

1. **Make Changes** to form configuration in dashboard
2. **Test Immediately** - changes reflect in real-time
3. **Verify Ordering** - drag-and-drop sections/fields
4. **Submit Test Application** - ensure data flows correctly
5. **Check Dashboard** - verify data appears correctly

## 📈 Performance Optimizations

- **Lazy Loading** - Form sections load progressively
- **Efficient Queries** - Optimized database operations
- **Caching** - Static assets are cached
- **Minified Assets** - Reduced file sizes
- **Background Processing** - File uploads don't block UI

## 🎯 Future Enhancements

- **Email Notifications** - Automated application confirmations
- **Advanced Analytics** - More detailed reporting
- **API Documentation** - Swagger/OpenAPI integration
- **Docker Support** - Containerized deployment
- **Cloud Storage** - S3/cloud file uploads

---

## 💡 Usage Tips

1. **Creating Sections:** Use descriptive names and choose appropriate icons
2. **Field Ordering:** Drag fields within sections for logical flow
3. **Validation Rules:** Use regex patterns for complex validation
4. **Testing:** Always test the form after making changes
5. **Backup:** Regular database backups recommended

**Happy Recruiting! 🎓✨**