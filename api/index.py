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
        # 使用模拟数据
        fortune_result = {
            'overall_fortune': '测试运势分析结果'
        }
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
    return render_template('result.html', 
        fortune={
            'overall_fortune': '测试运势分析结果'
        },
        user={
            'name': '测试用户'
        }
    ) 