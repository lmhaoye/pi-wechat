import os
import configparser
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    cf = configparser.ConfigParser()
    cf.read('app.conf')
    TOKEN = cf.get('wx','token')
    EA = ''
    APPID = cf.get('wx','appid')
    RAW = cf.getboolean('wx','Raw')

    REDIS_URL = cf.get('redis','url')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'test': TestingConfig
}