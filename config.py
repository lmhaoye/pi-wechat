import os
from ext import cf
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    TOKEN = cf.get('wx','token')
    APPID = cf.get('wx','appid')
    SECRET = cf.get('wx','secret')
    RAW = cf.getboolean('wx','Raw')
    EA = ''
    

    REDIS_URL = cf.get('redis','url')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'prod': ProdConfig
}