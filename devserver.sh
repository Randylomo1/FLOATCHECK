#!/bin/sh

# Activate the virtual environment
source .venv/bin/activate

# Start Redis server in the background
echo "Starting Redis..."
redis-server --daemonize yes

# Start Celery worker in the background
echo "Starting Celery worker..."
celery -A mysite worker -l info --detach

# Start the Django development server
echo "Starting Django development server..."
python mysite/manage.py runserver 0.0.0.0:$PORT
