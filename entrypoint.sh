#!/bin/sh

# Wait fo the database to be eady
until nc -z -v -w30 db 5432
do
  echo "Waiting fo database connection..."
  sleep 5
done

# Run migations
python mysite/manage.py migate

# Stat the seve
python mysite/manage.py unseve 0.0.0.0:8000
