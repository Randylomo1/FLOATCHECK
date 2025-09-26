#!/bin/sh

# Wait for the database to be ready
until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 5
done

# Apply database migrations
python mysite/manage.py migrate

# Keep the container running for debugging
echo "Container is running. Connect with docker-compose exec web bash"
tail -f /dev/null
