import sys
from pathlib import Path
import os

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from flask import Flask, render_template, request, jsonify, session
from core.ai_providers.factory import AIProviderFactory

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)

# 从环境变量获取密钥，如果没有则使用默认值
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_fortune():
    try:
        data = request.get_json(force=True)
        print("\n=== Starting analysis ===")
        print("Received data:", data)
        
        # 明确指定使用 mock provider
        provider = AIProviderFactory.create_provider('mock')
        print("Created provider:", provider.__class__.__name__)
        
        fortune_result = provider.generate_fortune(data)
        print("Raw fortune result:", fortune_result)  # 打印原始结果
        
        # 解析返回的文本，提取各个部分
        sections = {
            'overall_fortune': '暂无数据',
            'career_fortune': '暂无数据',
            'wealth_fortune': '暂无数据',
            'love_fortune': '暂无数据',
            'health_fortune': '暂无数据',
            'relationship_fortune': '暂无数据'
        }
        
        # 改进文本解析逻辑
        current_section = None
        current_content = []
        
        for line in fortune_result.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            print(f"Processing line: {line}")  # 调试每一行
            
            if '】：' in line:
                section_name = line.split('】：')[0].lstrip('【')
                content = line.split('】：')[1]
                
                print(f"Found section: {section_name}")  # 调试节点
                print(f"Content: {content}")  # 调试内容
                
                if section_name == '整体运势':
                    sections['overall_fortune'] = content
                elif section_name == '事业运势':
                    sections['career_fortune'] = content
                elif section_name == '财运分析':
                    sections['wealth_fortune'] = content
                elif section_name == '感情运势':
                    sections['love_fortune'] = content
                elif section_name == '健康提醒':
                    sections['health_fortune'] = content
                elif section_name == '人际关系':
                    sections['relationship_fortune'] = content
        
        print("Final parsed sections:", sections)  # 打印最终结果
        
        session['fortune_result'] = sections
        
        return jsonify({
            'status': 'success',
            'result': sections
        })
    except Exception as e:
        print(f"Error in analyze_fortune: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
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