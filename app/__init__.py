from flask import Flask
from config import config

from flask_redis import FlaskRedis


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #redis链接
    redis_store = FlaskRedis()

    redis_store.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .wechat import wechat as wechat_blueprint
    app.register_blueprint(wechat_blueprint)

    from .pi import pi as pi_blueprint
    app.register_blueprint(pi_blueprint)

    return app