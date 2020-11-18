from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1><a href = "/api/v1/hello-world-6"> Hello Word </a></h1>'


@app.route('/api/v1/hello-world-6')
def run():
    return '<h1> Hello world 6</h1>'


if __name__ == '__main__':
    serve(app, port=5000, host='0.0.0.0')
