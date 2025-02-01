from flask import Flask, render_template, request, jsonify, session

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
        # 使用完整的模拟数据
        fortune_result = {
            'overall_fortune': '整体运势良好，有上升趋势。',
            'career_fortune': '事业发展稳定，有新的机会。',
            'wealth_fortune': '财运平稳，注意理财规划。',
            'love_fortune': '感情运势上升，保持开放心态。',
            'health_fortune': '身体状况良好，注意作息。',
            'relationship_fortune': '人际关系和谐，多与人交流。'
        }
        # 将结果存储在会话中
        session['fortune_result'] = fortune_result
        return jsonify({
            'status': 'success',
            'result': fortune_result
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