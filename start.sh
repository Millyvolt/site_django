#!/bin/bash

# Exit on any error
set -e

echo "Starting minimal app for Railway..."

# Start the minimal app
echo "Starting minimal HTTP server..."
exec python app.py
