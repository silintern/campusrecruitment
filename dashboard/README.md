# Advanced Form Configuration System

This project implements a comprehensive, dynamic form configuration system for a recruitment dashboard. The system allows administrators to fully customize form fields, sections, validations, and more through an intuitive web interface.

## 🚀 Features Implemented

### 📝 Dynamic Form Management
- **Add/Delete Fields**: Administrators can add new form fields or remove existing ones (except core fields)
- **Field Types Supported**: 
  - Text, Email, Telephone, Date, Number
  - Textarea, Dropdown (Select), Radio Buttons, Checkboxes
  - File Upload
- **Real-time Database Updates**: All changes immediately reflect in the database and form rendering

### 🏗️ Section & Subsection Management
- **Flexible Sections**: Organize fields into logical sections and subsections
- **Section Renaming**: Easily rename sections across all associated fields
- **Auto-completion**: Existing sections appear as suggestions when creating new fields

### ✅ Field Configuration Options
- **Required/Optional Toggle**: Make any field required or optional with a simple checkbox
- **Field Ordering**: Drag-and-drop interface to reorder fields within the form
- **Field Labels**: Customize display names for all fields
- **Options Management**: Define dropdown options, radio button choices, etc.

### 🔍 Advanced Validation System
- **Length Validation**: Set minimum and maximum character limits
- **Pattern Validation**: Use regular expressions for complex validation rules
- **Custom Error Messages**: Define specific error messages for validation failures
- **Real-time Validation**: Client-side validation with immediate feedback

### 🎨 User Interface Features
- **Tabbed Interface**: Organized tabs for Fields Management, Sections & Order, and Validations
- **Drag & Drop**: Intuitive field reordering with visual feedback
- **Field Type Badges**: Color-coded badges for easy field type identification
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🔧 Technical Features
- **Database Schema Evolution**: Automatic database migrations for new fields
- **API-Driven**: RESTful APIs for all form configuration operations
- **Real-time Updates**: Changes reflect immediately without page refresh
- **Data Integrity**: Core fields protection and validation

## 🏛️ Architecture

### Backend (Flask)
- **Dynamic Schema Management**: Automatically adds/removes database columns
- **Form Configuration APIs**: Complete CRUD operations for form fields
- **Validation Engine**: Server-side validation with configurable rules
- **Data Migration**: Safe database schema updates

### Frontend (JavaScript + HTML)
- **Dynamic Form Rendering**: Generates forms based on database configuration
- **Interactive Configuration UI**: Rich interface for managing form structure
- **Client-side Validation**: Real-time field validation with custom rules
- **Modern UI Components**: Tailwind CSS for responsive design

### Database (SQLite)
- **Dynamic Schema**: Form configuration stored in `form_config` table
- **Flexible Applications Table**: Adapts to new fields automatically
- **Migration Support**: Safe schema evolution with data preservation

## 📊 Database Schema

### `form_config` Table
```sql
CREATE TABLE form_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,           -- Field name (database column)
    label TEXT NOT NULL,                 -- Display label
    type TEXT NOT NULL,                  -- Field type (text, select, etc.)
    subsection TEXT,                     -- Section/subsection name
    options TEXT,                        -- Comma-separated options for select/radio
    required BOOLEAN NOT NULL DEFAULT 0, -- Whether field is required
    is_core BOOLEAN NOT NULL DEFAULT 0,  -- Core fields cannot be deleted
    field_order INTEGER DEFAULT 0,       -- Display order
    validations TEXT DEFAULT '{}'        -- JSON validation rules
);
```

### Dynamic `applications` Table
The applications table automatically adapts its schema based on form configuration:
- Core fields: `id`, `name`, `email`, `submission_timestamp`, `resume_path`
- Dynamic fields: Added/removed based on form configuration

## 🔌 API Endpoints

### Form Configuration APIs
- `GET /api/form/config` - Get all form fields configuration
- `POST /api/form/config` - Add new form field
- `PUT /api/form/config/{id}` - Update existing form field
- `DELETE /api/form/config/{id}` - Delete form field (non-core only)
- `POST /api/form/config/reorder` - Reorder form fields
- `POST /api/form/config/bulk-update` - Bulk update field properties

### Public APIs
- `GET /api/public/form-config` - Get form structure for rendering (public)
- `POST /api/submit_application` - Submit form data

### Management APIs
- `GET /api/form/sections` - Get all form sections
- `GET /api/data` - Get dashboard data with filtering
- `POST /api/update_status` - Update application status

## 🎯 Usage Guide

### For Administrators

1. **Access Form Configuration**
   - Login to the dashboard
   - Click "Form Configuration" button
   - Navigate through the tabbed interface

2. **Add New Fields**
   - Go to "Fields Management" tab
   - Fill out the "Add New Field" form
   - Select field type and configure options
   - Set validation rules as needed

3. **Manage Field Order**
   - Switch to "Sections & Order" tab
   - Drag and drop fields to reorder
   - Click "Save Order" to apply changes

4. **Configure Validations**
   - Go to "Validations" tab
   - Set min/max length, patterns, and error messages
   - Changes save automatically

5. **Section Management**
   - Rename sections by clicking "Rename" in Sections tab
   - Create new sections by typing in the subsection field

### For Applicants

1. **Dynamic Form Experience**
   - Form loads configuration from database
   - Real-time validation feedback
   - Responsive design adapts to screen size
   - Error messages guide form completion

## 🔧 Configuration Options

### Field Types and Options

| Field Type | Options Required | Validation Support |
|------------|------------------|-------------------|
| Text       | No               | Length, Pattern   |
| Email      | No               | Pattern, Length   |
| Telephone  | No               | Pattern, Length   |
| Date       | No               | Custom validation |
| Number     | No               | Min/Max, Pattern  |
| Textarea   | No               | Length validation |
| Select     | Yes (comma-sep)  | Required only     |
| Radio      | Yes (comma-sep)  | Required only     |
| Checkbox   | No               | Required only     |
| File       | No               | File type/size    |

### Validation Rules (JSON Format)
```json
{
  "minLength": 5,
  "maxLength": 50,
  "pattern": "^[A-Za-z0-9]+$",
  "errorMessage": "Custom error message"
}
```

## 🚀 Getting Started

1. **Install Dependencies**
   ```bash
   pip3 install --break-system-packages -r requirements.txt
   pip3 install --break-system-packages flask-cors
   ```

2. **Start the Application**
   ```bash
   python3 app.py
   ```

3. **Access the Dashboard**
   - Navigate to `http://localhost:5000`
   - Login with default credentials:
     - Email: `admin@adventz.com`
     - Password: `12345`

4. **Configure Forms**
   - Click "Form Configuration" to start customizing
   - Add, edit, or remove fields as needed
   - Set up validation rules and field ordering

## 🔒 Security Features

- **Admin-only Access**: Form configuration requires admin privileges
- **Core Field Protection**: Essential fields cannot be deleted
- **Input Validation**: Both client and server-side validation
- **SQL Injection Prevention**: Parameterized queries throughout
- **File Upload Security**: Restricted file types and size limits

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface using Tailwind CSS
- **Responsive Layout**: Works on all device sizes
- **Interactive Elements**: Hover effects, animations, and transitions
- **Visual Feedback**: Loading states, success/error messages
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 📈 Performance Optimizations

- **Efficient Database Queries**: Optimized SQL with proper indexing
- **Client-side Caching**: Form configuration cached in browser
- **Lazy Loading**: Components load as needed
- **Minimal HTTP Requests**: Batch operations where possible

## 🔄 Data Flow

1. **Configuration Changes** → Database Update → UI Refresh
2. **Form Submission** → Validation → Database Storage → Dashboard Update
3. **Field Addition** → Schema Migration → Form Re-rendering
4. **Validation Rules** → Client-side Application → Server-side Verification

## 🛠️ Customization

The system is highly extensible:

- **New Field Types**: Add support for additional HTML input types
- **Custom Validations**: Implement complex validation logic
- **UI Themes**: Customize appearance with CSS modifications
- **Integration**: Connect with external systems via APIs

## 📝 Notes

- **Database Migrations**: Automatic and safe - no data loss
- **Field Dependencies**: Some fields may have interdependencies
- **Performance**: Optimized for forms with up to 100+ fields
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

This comprehensive form configuration system provides administrators with complete control over form structure while maintaining data integrity and user experience.