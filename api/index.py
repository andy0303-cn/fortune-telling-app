from http.server import BaseHTTPRequestHandler
import os
import json
from urllib.parse import urlparse, parse_qs

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Handling GET request for path: {self.path}")  # 调试信息
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/':
            try:
                content = read_file('templates/index.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error serving index.html: {str(e)}")  # 调试信息
                self.send_error(500, str(e))
        elif path == '/result':
            try:
                content = read_file('templates/result.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error serving result.html: {str(e)}")  # 调试信息
                self.send_error(500, str(e))
        elif path.startswith('/static/'):
            try:
                file_path = path[1:]  # 移除开头的 /
                print(f"Attempting to serve static file: {file_path}")  # 调试信息
                content = read_file(file_path)
                content_type = 'text/css' if path.endswith('.css') else 'application/javascript'
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error serving static file: {str(e)}")  # 调试信息
                self.send_error(404, str(e))
        else:
            print(f"Path not found: {path}")  # 调试信息
            self.send_error(404, "Not found")

    def do_POST(self):
        print(f"Handling POST request for path: {self.path}")  # 调试信息
        if self.path == '/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                user_data = json.loads(post_data.decode('utf-8'))
                print(f"Received user data: {user_data}")  # 调试信息

                result = {
                    'status': 'success',
                    'data': {
                        'overall': '运势平稳向上，保持积极心态，把握机遇。',
                        'career': '工作发展顺利，注意提升专业能力，保持良好的团队协作。',
                        'wealth': '财务状况稳定，建议合理规划支出，关注长期投资。',
                        'love': '感情生活和谐，保持真诚态度，增进情感交流。',
                        'health': '身体状况良好，注意作息规律，保持适度运动。',
                        'relationships': '人际关系融洽，多参与社交活动，深化重要友谊。'
                    }
                }

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                print("Successfully sent response")  # 调试信息
            except Exception as e:
                print(f"Error processing POST request: {str(e)}")  # 调试信息
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 