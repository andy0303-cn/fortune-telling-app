from http.server import BaseHTTPRequestHandler
import os
import json
from urllib.parse import urlparse, parse_qs
from fortune_analysis import FortuneAnalyzer

# API Version 1.0.1
# Last updated: 2024-02-02

def read_file(file_path):
    try:
        # 获取项目根目录
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_path, file_path)
        print(f"Attempting to read file: {full_path}")  # 调试信息
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")  # 调试信息
        raise

class handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.analyzer = FortuneAnalyzer()
        super().__init__(*args, **kwargs)

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

    async def do_POST(self):
        if self.path == '/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                user_data = json.loads(post_data.decode('utf-8'))
                print(f"Received POST data: {user_data}")  # 调试信息

                # 使用命理分析器生成结果
                result = await self.analyzer.analyze(user_data)

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