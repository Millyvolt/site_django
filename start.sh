#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput --settings=config.settings_production

# Run database migrations
python manage.py migrate --settings=config.settings_production

# Start the application
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --settings=config.settings_production
