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
        
        # 改进的文本解析
        current_section = None
        current_content = []
        
        for line in fortune_result.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('【'):
                if current_section and current_content:
                    content = ' '.join(current_content)
                    if current_section == '整体运势':
                        sections['overall_fortune'] = content
                    elif current_section == '事业运势':
                        sections['career_fortune'] = content
                    elif current_section == '财运分析':
                        sections['wealth_fortune'] = content
                    elif current_section == '感情运势':
                        sections['love_fortune'] = content
                    elif current_section == '健康提醒':
                        sections['health_fortune'] = content
                    elif current_section == '人际关系':
                        sections['relationship_fortune'] = content
                
                current_section = line[1:].split('】')[0]
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # 处理最后一个部分
        if current_section and current_content:
            content = ' '.join(current_content)
            if current_section == '整体运势':
                sections['overall_fortune'] = content
            elif current_section == '事业运势':
                sections['career_fortune'] = content
            elif current_section == '财运分析':
                sections['wealth_fortune'] = content
            elif current_section == '感情运势':
                sections['love_fortune'] = content
            elif current_section == '健康提醒':
                sections['health_fortune'] = content
            elif current_section == '人际关系':
                sections['relationship_fortune'] = content
        
        # 存储结果到会话
        session['fortune_result'] = sections
        
        return jsonify({
            'status': 'success',
            'result': sections
        })
    except Exception as e:
        app.logger.error(f"Error in analyze_fortune: {str(e)}")
        import traceback
        app.logger.error(f"Traceback: {traceback.format_exc()}")
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