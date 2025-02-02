from flask import Flask, render_template

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html', 
        fortune={
            'overall_fortune': '运势平稳向上。',
            'career_fortune': '工作发展顺利。',
            'wealth_fortune': '财务状况稳定。',
            'love_fortune': '感情生活和谐。',
            'health_fortune': '身体状况良好。',
            'relationship_fortune': '人际关系融洽。'
        },
        user={
            'name': '测试用户',
            'gender': 'M',
            'birth_date': '未知',
            'birth_place': '测试地点'
        }
    ) 