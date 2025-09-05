#!/usr/bin/env python3
"""
Enhanced minimal app with Django-like features for Railway deployment
"""
import os
import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health/' or self.path == '/':
            self.send_health_response()
        elif self.path == '/leetcode-daily/':
            self.send_leetcode_daily()
        elif self.path == '/leetcode-recent/':
            self.send_leetcode_recent()
        elif self.path == '/todos/':
            self.send_todos()
        else:
            self.send_404()
    
    def send_health_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'status': 'healthy', 
            'message': 'Django LeetCode App is running',
            'timestamp': datetime.now().isoformat(),
            'features': ['health', 'leetcode-daily', 'leetcode-recent', 'todos']
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def send_leetcode_daily(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Mock LeetCode daily data
        response = {
            'question': {
                'title': 'Two Sum',
                'difficulty': 'Easy',
                'acRate': 45.5,
                'frontendQuestionId': '1',
                'paidOnly': False,
                'topicTags': [{'name': 'Array'}, {'name': 'Hash Table'}]
            },
            'date': datetime.now().strftime('%Y-%m-%d'),
            'link': '/problems/two-sum',
            'user_status': 'NotAttempted',
            'error': None
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def send_leetcode_recent(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Mock recent questions data
        questions = [
            {
                'date': '2025-01-06',
                'link': '/problems/two-sum',
                'question': {
                    'title': 'Two Sum',
                    'difficulty': 'Easy',
                    'acRate': 45.5,
                    'frontendQuestionId': '1',
                    'paidOnly': False,
                    'topicTags': [{'name': 'Array'}, {'name': 'Hash Table'}]
                }
            },
            {
                'date': '2025-01-05',
                'link': '/problems/add-two-numbers',
                'question': {
                    'title': 'Add Two Numbers',
                    'difficulty': 'Medium',
                    'acRate': 35.2,
                    'frontendQuestionId': '2',
                    'paidOnly': False,
                    'topicTags': [{'name': 'Linked List'}, {'name': 'Math'}]
                }
            }
        ]
        
        response = {
            'questions': questions,
            'error': None
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def send_todos(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Mock todos data
        todos = [
            {
                'id': 1,
                'title': 'Complete Two Sum problem',
                'description': 'Solve the classic Two Sum problem on LeetCode',
                'priority': 'high',
                'status': 'pending',
                'due_date': None
            },
            {
                'id': 2,
                'title': 'Review dynamic programming',
                'description': 'Study DP patterns and practice problems',
                'priority': 'medium',
                'status': 'in_progress',
                'due_date': None
            }
        ]
        
        response = {
            'todos': todos,
            'message': 'Todo list loaded successfully'
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'error': 'Not found', 'message': 'The requested resource was not found'}
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server():
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), AppHandler)
    print(f"Starting Django LeetCode App server on port {port}")
    print("Available endpoints:")
    print("  /health/ - Health check")
    print("  /leetcode-daily/ - Daily LeetCode problem")
    print("  /leetcode-recent/ - Recent LeetCode problems")
    print("  /todos/ - Todo list")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
