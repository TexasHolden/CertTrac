# Cert.-Trac
Web App that tracks certification progress for ASC Tutors at Kent State University

Installation Steps
  Clone the Git Repository
  Clone the project using Git: git clone [repository-url]
  Set Up a Python Virtual Environment
  Navigate to the project directory.
  Create a virtual environment: python -m venv venv
  Activate the virtual environment:
  Windows: venv\Scripts\activate
  macOS/Linux: source venv/bin/activate

Install Dependencies
  Update pip: pip install --upgrade pip
  Install dependencies (if requirements.txt is available): pip install -r requirements.txt
  Configure Django Settings
  Configure database settings, security keys, and other settings in settings.py.
  Database Initialization
  Set up the database schema: python manage.py migrate

Static Files Configuration
  Ensure JS and CSS files are correctly referenced in your Django templates.
  Manage static files: python manage.py collectstatic


Run the Development Server
  Start the server: python manage.py runserver
  Access the application at http://localhost:8000.
