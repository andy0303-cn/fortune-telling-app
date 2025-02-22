from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
from urllib.parse import urlparse, parse_qs

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析 URL 和参数
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/':
            # 返回 index.html
            try:
                content = read_file('templates/index.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error reading index.html: {str(e)}")
                self.send_error(500, "Internal Server Error")
        elif path == '/static/css/style.css':
            # 返回 CSS 文件
            try:
                content = read_file('static/css/style.css')
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error reading style.css: {str(e)}")
                self.send_error(404, "File not found")
        elif path == '/static/js/main.js':
            # 返回 JavaScript 文件
            try:
                content = read_file('static/js/main.js')
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error reading main.js: {str(e)}")
                self.send_error(404, "File not found")
        elif path == '/result':
            # 返回结果页面
            try:
                content = read_file('templates/result.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error reading result.html: {str(e)}")
                self.send_error(500, "Internal Server Error")
        elif path == '/static/js/result.js':
            # 返回 result.js 文件
            try:
                content = read_file('static/js/result.js')
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                print(f"Error reading result.js: {str(e)}")
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/analyze':
            # 读取 POST 数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user_data = json.loads(post_data.decode('utf-8'))

            # 生成分析结果
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

            # 返回 JSON 响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_error(404, "Not found")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run() 