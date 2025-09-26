#!/bin/sh

# Wait for the database to be ready
until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 5
done

# Apply database migrations
python mysite/manage.py migrate

# Start Gunicorn
gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
