from API import app


@app.route('/')
def index():
    return '<h1><a href = "/api/v1/hello-world-6"> Hello Word </a></h1>'


@app.route('/api/v1/hello-world-6')
def run():
    return '<h1> Hello world 6</h1>'


