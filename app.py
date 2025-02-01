from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import Config
import mysql.connector
from datetime import datetime
import logging
from core.deepseek_agent import FortuneAgent
import json
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 设置日志
logging.basicConfig(level=logging.DEBUG)

# 添加JSON编码器
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

app = Flask(__name__)
app.config.from_object(Config)
app.json_encoder = CustomJSONEncoder  # 使用自定义的JSON编码器

# 设置响应的默认字符集
app.config['JSON_AS_ASCII'] = False

# 从环境变量读取配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB', 'fortune_telling')
}

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def get_db():
    try:
        # 使用环境变量中的数据库配置
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB', 'fortune_telling'),
            auth_plugin='caching_sha2_password'
        )
        logging.debug("Database connection successful")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_fortune():
    try:
        data = request.get_json(force=True)
        fortune_agent = FortuneAgent(test_mode=True)
        fortune_result = fortune_agent.analyze_fortune(data)
        return jsonify({
            'status': 'success',
            'result': fortune_result
        })
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '分析过程中出现错误'
        }), 500

@app.route('/result')
def result():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 获取最新的用户信息和运势分析
        cursor.execute("""
            SELECT u.name, u.gender, u.birth_date, u.birth_place,
                   fr.overall_fortune, fr.career_fortune, fr.wealth_fortune,
                   fr.love_fortune, fr.health_fortune, fr.relationship_fortune
            FROM users u
            JOIN fortune_readings fr ON u.id = fr.user_id
            ORDER BY fr.created_at DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if not result:
            return "未找到运势分析结果", 404
            
        return render_template('result.html', fortune=result, user=result)
    except Exception as e:
        logging.error(f"获取运势结果失败: {str(e)}")
        return "获取运势结果失败", 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

@app.errorhandler(500)
def handle_500_error(error):
    logging.error(f"Internal error: {error}")
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误，请稍后重试'
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    logging.error(f"Unhandled exception: {error}")
    return jsonify({
        'status': 'error',
        'message': '发生未知错误，请稍后重试'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 