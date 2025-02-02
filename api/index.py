import sys
import os
from flask import Flask

app = Flask(__name__)

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