# Quick Start Guide - Path2Prep

## Running the Project

### Backend (Django)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies (if not already done):**
   ```bash
   pip install Django djangorestframework django-cors-headers djangorestframework-simplejwt django-filter psycopg2-binary pymongo celery redis django-ratelimit
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the server:**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at: **http://localhost:8000**

### Frontend (React)

1. **Navigate to frontend directory:**
   ```bash
   cd path2prep
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   Frontend will be available at: **http://localhost:3000**

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

## Notes

- The project uses SQLite by default for development (no PostgreSQL setup needed)
- ML/NLP features will work in basic mode without additional dependencies
- To enable full ML features, install: `numpy pandas scikit-learn tensorflow transformers sentence-transformers spacy`
- MongoDB and Redis are optional for basic functionality

## Troubleshooting

- If you see database errors, delete `backend/db.sqlite3` and run migrations again
- If imports fail, make sure all dependencies are installed
- For ML features, you may need to install spaCy model: `python -m spacy download en_core_web_sm`

