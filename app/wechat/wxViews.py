from . import wechat

from ext import redis, cf, wechat_client

@wechat.route('/wechat/access_token')
def accessToken():
    at = wechat_client.access_token
    return at or 'not get access_token'
