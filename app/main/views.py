from . import main

from flask import request, abort, render_template, current_app

@main.route('/')
def index():
    host = request.url_root
    return render_template('index.html', host=host)

@main.route('/get/ip')
def getIp():
    real_ip = request.headers.get('X-Real-Ip', request.remote_addr)
    return real_ip