#!/bin/sh

# Wait for the PostgreSQL database to be ready
/wait-for-it.sh db:5432 --strict --timeout=60 -- echo "Database is up"

# Run Django management commands
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000