from flask import Flask, Response

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response('Hello from Vercel!', mimetype='text/plain')

# Vercel 需要这个处理程序
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run() 