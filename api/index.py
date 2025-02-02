from http.server import BaseHTTPRequestHandler
import os
import json
from urllib.parse import urlparse, parse_qs

# API Version 1.0.1
# Last updated: 2024-02-02

def read_file(file_path):
    # 获取项目根目录
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_path, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

class handler(BaseHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        print(f"Request: {self.command} {self.path} {code}")

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        try:
            if path == '/':
                content = read_file('templates/index.html')
                content_type = 'text/html'
            elif path == '/result':
                content = read_file('templates/result.html')
                content_type = 'text/html'
            elif path.startswith('/static/'):
                file_path = path[1:]  # 移除开头的 /
                content = read_file(file_path)
                content_type = 'text/css' if path.endswith('.css') else 'application/javascript'
            else:
                raise FileNotFoundError(f"File not found: {path}")

            self.send_response(200)
            self.send_header('Content-type', f'{content_type}; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode())
            print(f"Successfully served {path}")  # 调试信息

        except Exception as e:
            print(f"Error handling request: {str(e)}")
            if isinstance(e, FileNotFoundError):
                self.send_error(404, str(e))
            else:
                self.send_error(500, str(e))

    def do_POST(self):
        if self.path == '/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                user_data = json.loads(post_data.decode('utf-8'))
                print(f"Received POST data: {user_data}")  # 调试信息

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
                print("Successfully sent analysis result")  # 调试信息

            except Exception as e:
                print(f"Error processing POST request: {str(e)}")
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 