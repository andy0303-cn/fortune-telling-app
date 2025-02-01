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
        # 使用纯密码认证
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='cl50332067',
            database='fortune_telling',
            auth_plugin='caching_sha2_password'  # 使用新的认证插件
        )
        logging.debug("Database connection successful")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist")
        else:
            logging.error(err)
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_fortune():
    try:
        data = request.get_json(force=True)  # 强制解析JSON
        logging.debug(f"Received data: {data}")
        
        # 确保所有字符串都是UTF-8编码
        data = {k: v.encode('utf-8').decode('utf-8') if isinstance(v, str) else v 
               for k, v in data.items()}
        
        # 尝试连接数据库
        try:
            db = get_db()
            logging.debug("Database connection established")
        except Exception as e:
            logging.error(f"Failed to connect to database: {str(e)}")
            return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
        
        cursor = db.cursor()
        
        # 记录SQL语句
        sql = """INSERT INTO users (name, gender, birth_date, birth_place)
                 VALUES (%s, %s, %s, %s)"""
        values = (data['name'], data['gender'], data['birthDate'], data['birthPlace'])
        logging.debug(f"Executing SQL: {sql} with values: {values}")
        
        cursor.execute(sql, values)
        user_id = cursor.lastrowid
        
        # 生成运势分析
        fortune_agent = FortuneAgent(test_mode=True)  # 启用测试模式
        fortune_result = fortune_agent.analyze_fortune(data)
        logging.debug(f"Generated fortune result: {fortune_result}")  # 添加日志

        # 将结果保存到数据库
        insert_fortune_sql = """
            INSERT INTO fortune_readings (
                user_id, reading_date, overall_fortune, career_fortune,
                wealth_fortune, love_fortune, health_fortune, relationship_fortune
            ) VALUES (%s, CURDATE(), %s, %s, %s, %s, %s, %s)
        """
        fortune_values = (
            user_id,
            fortune_result['overall_fortune'],
            fortune_result['career_fortune'],
            fortune_result['wealth_fortune'],
            fortune_result['love_fortune'],
            fortune_result['health_fortune'],
            fortune_result['relationship_fortune']
        )
        logging.debug(f"Executing fortune insert SQL with values: {fortune_values}")  # 添加日志
        
        cursor.execute(insert_fortune_sql, fortune_values)
        db.commit()  # 移动到这里，确保两个插入都成功
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'message': '运势分析完成！'  # 添加用户友好的消息
        })
    except Exception as e:
        logging.error(f"Error in analyze_fortune: {str(e)}")
        if 'db' in locals():
            db.rollback()
        return jsonify({
            'status': 'error',
            'message': '抱歉，分析过程中出现错误，请稍后重试。'  # 用户友好的错误消息
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 