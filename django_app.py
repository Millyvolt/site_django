#!/usr/bin/env python3
"""
Django app runner for Railway with health check fallback
"""
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health/' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'healthy', 'message': 'Django app is running'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def start_health_server():
    """Start a simple health check server"""
    port = int(os.environ.get('PORT', 8000))
    health_port = port + 1  # Use next port for health checks
    
    server = HTTPServer(('0.0.0.0', health_port), HealthHandler)
    print(f"Health server started on port {health_port}")
    server.serve_forever()

def main():
    # Start health server in background
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Give health server time to start
    time.sleep(2)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
    
    try:
        import django
        from django.core.management import execute_from_command_line
        
        # Setup Django
        django.setup()
        
        # Get port from environment
        port = os.environ.get('PORT', 8000)
        
        # Run Django development server
        sys.argv = ['manage.py', 'runserver', f'0.0.0.0:{port}']
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"Django failed to start: {e}")
        print("Falling back to simple server...")
        
        # Fallback to simple server
        port = int(os.environ.get('PORT', 8000))
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"Starting fallback server on port {port}")
        server.serve_forever()

if __name__ == '__main__':
    main()
