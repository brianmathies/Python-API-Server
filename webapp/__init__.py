from flask import Flask
from config import  config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    from webapp.mod_auth import mod_auth as mod_auth_blueprint

    app.register_blueprint(mod_auth_blueprint,url_prefix="/v1")


    return app