from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, Butt!'


@app.route('/about')
def about():
    return 'This is a Flask learning app.'
