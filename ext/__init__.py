from redis import Redis
import configparser

from wechatpy.client import WeChatClient
from wechatpy.session.redisstorage import RedisStorage

cf = configparser.ConfigParser()
cf.read('app.conf')

redis = Redis.from_url(cf.get('redis','url'))

session_interface = RedisStorage(
    redis,
    prefix="wechatpy"
)

wechat_client = WeChatClient(
    cf.get('wx','appid'),
    cf.get('wx','secret'),
    session=session_interface
)