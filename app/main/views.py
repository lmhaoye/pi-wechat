from . import main

from flask import request, abort, render_template, current_app

@main.route('/')
def index():
    host = request.url_root
    return render_template('index.html', host=host)

@main.route('/test')
def test():
    return current_app.config['TOKEN']