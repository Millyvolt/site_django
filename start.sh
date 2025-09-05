#!/bin/bash

# Exit on any error
set -e

echo "Starting Django deployment..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings_production

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --settings=config.settings_production

# Start the application
echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --settings=config.settings_production --timeout 120 --workers 2
