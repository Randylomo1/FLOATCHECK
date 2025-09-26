#!/bin/bash

# Stop any currently running services and remove them to ensure a clean start.
docker-compose down

# Bring up all services defined in docker-compose.yml.
# --build: Rebuild images if files have changed.
# The `command` in docker-compose.yml will handle waiting for the DB and migrating.
docker-compose up --build
