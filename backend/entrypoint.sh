#!/bin/sh

python manage.py migrate --noinput

# Start server
echo "Starting server"

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=4

python manage.py bot

# run the container CMD
exec "$@"