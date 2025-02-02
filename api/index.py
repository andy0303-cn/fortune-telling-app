from flask import Flask, render_template, request, jsonify

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_fortune():
    try:
        data = request.get_json(force=True)
        
        # 返回固定的测试数据
        result = {
            'overall_fortune': '运势平稳向上，保持积极心态，把握机遇。',
            'career_fortune': '工作发展顺利，注意提升专业能力，保持良好的团队协作。',
            'wealth_fortune': '财务状况稳定，建议合理规划支出，关注长期投资。',
            'love_fortune': '感情生活和谐，保持真诚态度，增进情感交流。',
            'health_fortune': '身体状况良好，注意作息规律，保持适度运动。',
            'relationship_fortune': '人际关系融洽，多参与社交活动，深化重要友谊。'
        }
        
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/result')
def result():
    return render_template('result.html', 
        fortune={
            'overall_fortune': '运势平稳向上，保持积极心态，把握机遇。',
            'career_fortune': '工作发展顺利，注意提升专业能力，保持良好的团队协作。',
            'wealth_fortune': '财务状况稳定，建议合理规划支出，关注长期投资。',
            'love_fortune': '感情生活和谐，保持真诚态度，增进情感交流。',
            'health_fortune': '身体状况良好，注意作息规律，保持适度运动。',
            'relationship_fortune': '人际关系融洽，多参与社交活动，深化重要友谊。'
        },
        user={
            'name': request.args.get('name', '测试用户'),
            'gender': request.args.get('gender', 'M'),
            'birth_date': request.args.get('birthdate', '未知'),
            'birth_place': request.args.get('birthplace', '测试地点')
        }
    ) 