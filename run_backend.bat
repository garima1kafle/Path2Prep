@echo off
echo Setting up Path2Prep Backend...
cd backend

echo Installing Python dependencies...
pip install -r requirements.txt

echo Running database migrations...
python manage.py migrate

echo Creating superuser (if needed)...
echo Note: You can skip this if superuser already exists
python manage.py createsuperuser --noinput 2>nul || echo Superuser creation skipped

echo Starting Django development server...
python manage.py runserver

