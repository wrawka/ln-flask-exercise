from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def home():
    context = {
        'name': 'Patato'
    }
    return render_template('home.html', context=context)


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        context = request.form
        return render_template('your_url.html', context=context)
    return '☹️ This is not valid.'