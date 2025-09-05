#!/bin/bash

# Exit on any error
set -e

echo "Starting Django app for Railway..."

# Start the Django app
echo "Starting Django application..."
exec python django_app.py
