from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Flask 快速示例<h1>'
