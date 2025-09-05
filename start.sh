#!/bin/bash

# Exit on any error
set -e

echo "Starting Django deployment..."

# Start the application directly
echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --settings=config.settings_production --timeout 120 --workers 1 --preload
