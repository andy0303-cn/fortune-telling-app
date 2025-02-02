from http.server import BaseHTTPRequestHandler
import os

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
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
        elif self.path == '/static/css/style.css':
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
        else:
            self.send_error(404, "File not found") 