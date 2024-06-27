#!/bin/sh

python manage.py migrate --noinput

# Сборка статических файлов Django
python manage.py collectstatic --noinput --clear

# Start server
echo "Starting server"

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=4

# Start server
echo "Starting bot"

python manage.py start_bot

# run the container CMD
exec "$@"