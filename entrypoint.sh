#!/bin/sh

# Wait for the database container to be ready
echo "Waiting for database connection..."
until nc -z -v -w30 db 5432
do
  echo "Retrying database connection..."
  sleep 5
done
echo "Database is ready."

# Apply database migrations
echo "Applying database migrations..."
python mysite/manage.py migrate
echo "Migrations applied."

# The "$@" executes the command passed as the CMD in the Dockerfile
# In this case, it will run: gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
exec "$@"
