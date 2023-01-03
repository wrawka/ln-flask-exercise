import json
import os
from flask import abort, Flask, flash, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random_string'

URLS_FILE = 'urls.json'


@app.route('/')
def home():
    context = {
        'name': 'Potato',
        'slugs': session.keys()
    }
    return render_template('home.html', context=context)


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        url = request.form.get('url')

        if os.path.exists(URLS_FILE):
            with open(URLS_FILE, 'r') as url_file:
                urls = json.load(url_file)
        
        slug = request.form.get('slug')

        if slug in urls.keys():
            flash(f'Slug "{slug}" has already been taken. Please think of a new one.')
            return redirect('/')
        
        if url:
            urls[slug] = {'url': url}

        file = request.files.get('file')

        if file:
            full_filename = f'{slug}_{secure_filename(file.filename)}'
            file.save('/'.join((os.getcwd(), 'static', 'uploads', full_filename)))  #TODO: refactor to pathlib
            urls[slug] = {'file': full_filename}

        with open(URLS_FILE, 'w') as url_file:
            json.dump(urls, url_file, indent=4)
            session[slug] = True
            return render_template('your_url.html', context={'slug': slug, 'url': url})

    return redirect('/')


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@app.route('/<string:slug>')
def redirect_to_url(slug):
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'r') as url_file:
            urls = json.load(url_file)
            if slug in urls.keys():
                if 'url' in urls[slug].keys():
                    return redirect(urls[slug]['url'])
                if 'file' in urls[slug].keys():
                    return redirect(url_for('static', filename='uploads/' + urls[slug]['file']))
    return abort(404)


@app.errorhandler(404)
def page_not_foud(error):
    return render_template('page_not_found.html'), 404
