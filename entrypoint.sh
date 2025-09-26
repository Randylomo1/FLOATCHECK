#!/bin/sh

# Wait for the database to be ready
until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 5
done

# Run migrations
python mysite/manage.py migrate

# Start the server
# python mysite/manage.py runserver 0.0.0.0:8000 --noreload

echo "Entrypoint script finished. Starting sleep..."
sleep infinity
