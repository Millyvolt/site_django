#!/bin/bash

# Exit on any error
set -e

echo "Starting Django deployment..."

# Start the application with Django's development server for Railway
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:$PORT --settings=config.settings_production
