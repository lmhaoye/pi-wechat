from . import pi

from flask import request, abort, current_app

@pi.route('/pi/ip',methods=['Get'])
def pi_ip_get():
    return ''