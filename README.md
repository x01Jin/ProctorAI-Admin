# ProctorAI Administrator Interface

An administrative interface for managing proctors and exam reports for The ProctorAI application.

## System Requirements

- MySQL Database
- Operating System: Windows

## Features

### Authentication

- Secure login system for administrators
- Role-based access control

### Proctor Management

- View list of all proctors
- Add new proctors
- Edit existing proctor details
- Delete proctors with confirmation
- View detailed proctor profiles

#### Proctor Editor

- Fixed dialog size: 340x220 pixels
- Required fields:
  - Proctor Name (unique)
  - Email (unique)
  - Password (with secure input)
- Form validation ensures all fields are filled
- Success/error feedback through dialog boxes

### Report Management

- View exam reports by proctor
- Track exam sessions with detailed information
- Monitor proctor assignments and schedules

### User Interface

- Dark theme using Qt Fusion style
- Split-panel layout:
  - Left: Proctor list (minimum width 300px)
  - Right: Profile and reports view
- Responsive design with minimum window size 1280x720
- Context menu actions for proctor management
- Real-time updates on data changes

## Security

- Password encryption for user credentials
- Role-based access control system
- Database connection security through MySQL connector
- Secure password input fields
- Input validation to prevent SQL injection
- Unique constraints on critical fields

## Error Handling

- Validation feedback for required fields
- Database operation error reporting
- User-friendly error messages
- Transaction rollback on failures

## Application Structure

```File Structure
ProctorAI-Admin/
├── backend/
│   ├── auth.py         # Authentication system
│   └── db.py          # Database operations
├── frontend/
│   ├── proctor_editor.py  # Proctor creation/editing
│   ├── proctor_list.py    # List of proctors
│   ├── proctor_profile.py # Proctor details view
│   ├── report_list.py     # Exam reports view
│   ├── toolbar.py         # Application toolbar
│   └── utils.py          # Utility functions
├── themes/
│   └── theme.py         # UI theming
├── main.py             # Application entry point
└── proctorai.sql      # Database schema
```

## Database Schema

### Users Table

- Primary key: `id` (auto-increment)
- `proctor_name`: Unique proctor identifier
- `email`: Unique email address
- `password`: Encrypted password
- `user_role`: Either 'admin' or 'proctor'

### ReportLog Table

- Primary key: `id` (auto-increment)
- `user_id`: Foreign key to users table
- Exam details:
  - `num_students`: Number of students
  - `block`: Time block
  - `subject`: Exam subject
  - `room`: Exam location
  - `start`: Start time
  - `end`: End time
  - `date`: Exam date
