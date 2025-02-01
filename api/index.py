from flask import Flask, render_template, request, jsonify, session
from core.ai_providers.factory import AIProviderFactory

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)
app.config['SECRET_KEY'] = 'your-secret-key'  # 用于会话加密

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_fortune():
    try:
        data = request.get_json(force=True)
        
        # 使用工厂创建 AI Provider（默认使用 mock）
        provider = AIProviderFactory.create_provider()
        fortune_result = provider.generate_fortune(data)
        
        # 解析返回的文本，提取各个部分
        sections = {
            'overall_fortune': '暂无数据',
            'career_fortune': '暂无数据',
            'wealth_fortune': '暂无数据',
            'love_fortune': '暂无数据',
            'health_fortune': '暂无数据',
            'relationship_fortune': '暂无数据'
        }
        
        # 简单的文本解析
        current_section = None
        for line in fortune_result.split('\n'):
            line = line.strip()
            if line.startswith('【') and line.endswith('】：'):
                current_section = line[1:-2]  # 移除【】：
                continue
            if current_section and line:
                if current_section == '整体运势':
                    sections['overall_fortune'] = line
                elif current_section == '事业运势':
                    sections['career_fortune'] = line
                elif current_section == '财运分析':
                    sections['wealth_fortune'] = line
                elif current_section == '感情运势':
                    sections['love_fortune'] = line
                elif current_section == '健康提醒':
                    sections['health_fortune'] = line
                elif current_section == '人际关系':
                    sections['relationship_fortune'] = line
        
        # 存储结果到会话
        session['fortune_result'] = sections
        
        return jsonify({
            'status': 'success',
            'result': sections
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/result')
def result():
    # 从会话中获取运势结果
    fortune_result = session.get('fortune_result', {
        'overall_fortune': '暂无运势分析结果'
    })
    return render_template('result.html', 
        fortune=fortune_result,
        user={
            'name': request.args.get('name', '测试用户'),
            'gender': request.args.get('gender', 'M'),
            'birth_date': request.args.get('birthdate', '未知'),  # 直接使用传入的格式化日期
            'birth_place': request.args.get('birthplace', '测试地点')
        }
    ) 