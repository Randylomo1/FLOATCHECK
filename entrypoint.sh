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

# Execute the CMD from the Dockerfile (i.e., start Gunicorn)
exec "$@"
