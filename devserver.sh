#!/bin/bash

# Source the .env file to load environment variables
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Bring up the database service in the background
docker-compose up -d db

# Run the web service, executing the entrypoint script
# This ensures the db is ready and migrations run before starting the server.
docker-compose run --service-ports web /app/entrypoint.sh
