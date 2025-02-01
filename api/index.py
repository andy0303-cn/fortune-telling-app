from flask import Flask, render_template, request, jsonify
import os
import logging
import json
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['JSON_AS_ASCII'] = False

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_fortune():
    try:
        data = request.get_json(force=True)
        # 使用模拟数据而不是调用 AI API
        fortune_result = {
            'overall_fortune': '整体运势良好，有上升趋势。',
            'career_fortune': '事业发展稳定，有新的机会。',
            'wealth_fortune': '财运平稳，注意理财规划。',
            'love_fortune': '感情运势上升，保持开放心态。',
            'health_fortune': '身体状况良好，注意作息。',
            'relationship_fortune': '人际关系和谐，多与人交流。'
        }
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
        # 使用 session 或 临时存储来获取分析结果
        return render_template('result.html', 
            fortune={
                'overall_fortune': '整体运势分析结果',
                'career_fortune': '事业运势分析结果',
                'wealth_fortune': '财运分析结果',
                'love_fortune': '感情运势分析结果',
                'health_fortune': '健康运势分析结果',
                'relationship_fortune': '人际关系分析结果'
            },
            user={
                'name': '测试用户',
                'gender': 'M',
                'birth_date': '2024-02-01',
                'birth_place': '测试地点'
            }
        )
    except Exception as e:
        logging.error(f"获取运势结果失败: {str(e)}")
        return "获取运势结果失败", 500

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

# 确保导出 app 变量给 Vercel
app = app

# 修改处理函数
def handler(request):
    """Handle incoming requests."""
    try:
        logger.debug(f"Received request: {request}")
        return app
    except Exception as e:
        logger.error(f"Handler error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'message': str(e)
            })
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 