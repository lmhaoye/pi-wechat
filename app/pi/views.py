from . import pi

from app import redis_store

from flask import request, abort, current_app


@pi.route('/pi/ip',methods=['Get'])
def pi_ip_get():
    return redis_store.get('pi_ip') or 'not set'

@pi.route('/pi/ip',methods=['POST'])
def pi_ip_post():
    ip = request.form['ip'];
    rs =  redis_store.set('pi_ip',ip)
    if rs:
        return 'success'
    else:
        return 'fail'