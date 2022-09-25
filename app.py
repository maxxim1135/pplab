from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/hello-world-7')
def hello_world():
    return "<strong>Hello World 7!</strong>"


if __name__ == '__main__':
    app.run()
