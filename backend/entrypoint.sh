#!/bin/sh

# Apply database migrations
python manage.py migrate --noinput

# Load fixtures
echo "Loading fixtures"
python manage.py loaddata fixtures/ab.json

# Collect static files
python manage.py collectstatic --noinput --clear

# Start the bot in the background
echo "Starting bot"
python manage.py start_bot --noinput --clear &

# Start Gunicorn server
echo "Starting server"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=4

# run the container CMD
exec "$@"
