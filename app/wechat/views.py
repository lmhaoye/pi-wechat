from . import wechat

from app import redis_store

from flask import request, abort, current_app
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException



@wechat.route('/wechat', methods=['GET', 'POST'])
def wechatView():

    TOKEN = current_app.config['TOKEN']
    EncodingAESKey = current_app.config['EA']
    AppId = current_app.config['APPID']
    Raw = current_app.config['RAW']

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
        		reply = create_reply(redis_store.get('pi_ip'), msg)
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