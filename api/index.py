import sys
import os
from flask import Flask

def application(env, start_response):
    """最简单的 WSGI 应用"""
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello World']

app = application

@app.route('/')
def index():
    # 打印环境信息
    python_version = sys.version
    python_path = sys.path
    current_dir = os.getcwd()
    env_vars = dict(os.environ)
    
    return f"""
    Python Version: {python_version}
    Python Path: {python_path}
    Current Directory: {current_dir}
    Environment Variables: {env_vars}
    """

# 添加错误处理
@app.errorhandler(500)
def handle_500(e):
    return str(e), 500 