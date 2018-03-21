from __future__ import absolute_import, unicode_literals
import configparser
from flask import Flask, request, abort, render_template
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException

# set token or get from environments
# TOKEN = os.getenv('WECHAT_TOKEN', 'BGZ7ATTFKHASYYLO')
# EncodingAESKey = os.getenv('WECHAT_ENCODING_AES_KEY', '')
# AppId = os.getenv('WECHAT_APP_ID', 'wxc7531fa470e0f0e7')
cf = configparser.ConfigParser()
cf.read('app.conf')

TOKEN = cf.get('wx','token')
EncodingAESKey = ''
AppId = cf.get('wx','appid')
Raw = cf.getboolean('wx','Raw')

app = Flask(__name__)


@app.route('/')
def index():
    host = request.url_root
    return render_template('index.html', host=host)

@app.route('/pi/ip',methods=['GET','POST'])
def piIp():
    if request.method == 'GET':
        with open('./ip.txt',mode='r',encoding='utf-8') as f:
            return f.read()
    else:
        ip = request.form['ip']
        print('record ip:%s' % ip)
        with open('./ip.txt',mode='w+',encoding='utf-8') as f:
            f.write(ip)
        return 'ok'
def getIp():
	with open('./ip.txt',mode='r',encoding='utf-8') as f:
            return f.read()


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    encrypt_type = request.args.get('encrypt_type', '')
    msg_signature = request.args.get('msg_signature', '')

    print('signature:', signature)
    print('timestamp: ', timestamp)
    print('nonce:', nonce)
    print('echo_str:', echo_str)
    print('encrypt_type:', encrypt_type)
    print('msg_signature:', msg_signature)

    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        return echo_str
    else:
        if Raw:
            print('Raw message: \n%s' % request.data)
            crypto = WeChatCrypto(TOKEN, EncodingAESKey, AppId)
            try:
                msg = crypto.decrypt_message(
                    request.data,
                    msg_signature,
                    timestamp,
                    nonce
                )
                print('Descypted message: \n%s' % msg)
            except (InvalidSignatureException, InvalidAppIdException):
                abort(403)
        else:
            msg = request.data
        msg = parse_message(msg)

        print('request data:\n%s' % msg)

        if msg.type == 'text':
        	if msg.content == 'ip':
        		reply = create_reply(getIp(), msg)
        	else:
        		reply = create_reply(msg.content, msg)
        elif msg.type == 'voice':
            reply = create_reply('voice msg',msg)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
        if Raw:
            return crypto.encrypt_message(
                reply.render(),
                nonce,
                timestamp
            )
        else:
            return reply.render()

if __name__ == '__main__':
    app.run('127.0.0.1', 5001, debug=True)