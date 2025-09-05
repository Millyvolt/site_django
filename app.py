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
        if self.path == '/health/':
            self.send_health_response()
        elif self.path == '/' or self.path == '/index.html':
            self.send_home_page()
        elif self.path == '/leetcode-daily/':
            self.send_leetcode_daily()
        elif self.path == '/leetcode-recent/':
            self.send_leetcode_recent()
        elif self.path == '/todos/':
            self.send_todos()
        else:
            self.send_404()
    
    def send_home_page(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django LeetCode Site</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .nav-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .nav-card {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 25px;
            text-align: center;
            transition: transform 0.3s ease, background 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
            text-decoration: none;
            color: white;
            display: block;
        }
        .nav-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
        }
        .nav-card h3 {
            margin: 0 0 15px 0;
            font-size: 1.5em;
        }
        .nav-card p {
            margin: 0;
            opacity: 0.9;
        }
        .status {
            background: rgba(76, 175, 80, 0.3);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        .status h2 {
            margin: 0 0 10px 0;
            color: #4CAF50;
        }
        .feature-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 15px;
        }
        .feature-tag {
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Django LeetCode Site</h1>
        
        <div class="status">
            <h2>✅ Site Status: Online</h2>
            <p>Your Django LeetCode application is successfully deployed and running!</p>
            <div class="feature-list">
                <span class="feature-tag">Health Check</span>
                <span class="feature-tag">LeetCode Daily</span>
                <span class="feature-tag">LeetCode Recent</span>
                <span class="feature-tag">Todo Management</span>
            </div>
        </div>

        <div class="nav-grid">
            <a href="/health/" class="nav-card">
                <h3>🏥 Health Check</h3>
                <p>Check the application status and system information</p>
            </a>
            
            <a href="/leetcode-daily/" class="nav-card">
                <h3>📅 LeetCode Daily</h3>
                <p>View today's LeetCode problem and challenge yourself</p>
            </a>
            
            <a href="/leetcode-recent/" class="nav-card">
                <h3>📚 LeetCode Recent</h3>
                <p>Browse recent LeetCode problems and solutions</p>
            </a>
            
            <a href="/todos/" class="nav-card">
                <h3>✅ Todo List</h3>
                <p>Manage your coding tasks and track progress</p>
            </a>
        </div>

        <div style="text-align: center; margin-top: 40px; opacity: 0.8;">
            <p>🌐 Successfully deployed on Railway • Made with Django</p>
        </div>
    </div>
</body>
</html>"""
        
        self.wfile.write(html_content.encode())
    
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
