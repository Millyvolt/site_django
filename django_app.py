#!/usr/bin/env python3
"""
Django app runner for Railway
This is a more robust Django startup script
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
    
    # Setup Django
    django.setup()
    
    # Get port from environment
    port = os.environ.get('PORT', 8000)
    
    # Run Django development server
    sys.argv = ['manage.py', 'runserver', f'0.0.0.0:{port}']
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
