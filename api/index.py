from http.server import BaseHTTPRequestHandler
import os
import json
from urllib.parse import urlparse, parse_qs

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
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
                self.send_error(500, str(e))
        elif path == '/result':
            try:
                content = read_file('templates/result.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_error(500, str(e))
        elif path.startswith('/static/'):
            try:
                content = read_file(path[1:])  # 移除开头的 /
                content_type = 'text/css' if path.endswith('.css') else 'application/javascript'
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_error(404, str(e))
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        if self.path == '/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                user_data = json.loads(post_data.decode('utf-8'))

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

                # 返回重定向响应
                self.send_response(303)  # 303 See Other
                self.send_header('Location', '/result')
                self.end_headers()
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 