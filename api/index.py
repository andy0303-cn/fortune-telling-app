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
            'overall_fortune': '测试运势分析结果'
        },
        user={
            'name': '测试用户'
        }
    ) 