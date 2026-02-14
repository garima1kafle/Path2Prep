@echo off
set DJANGO_ENV=development
cd /d %~dp0
python manage.py migrate
python manage.py runserver

