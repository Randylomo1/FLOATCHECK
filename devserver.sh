#!/bin/bash

# Source the .env file to load environment variables
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Start all services
docker-compose up
