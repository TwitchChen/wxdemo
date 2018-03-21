# encoding: utf-8

from flask import Flask
from config_loc import config,env
from flask_sqlalchemy import SQLAlchemy
import flask_logger

"""
@author: Twitch Chen
@file: __init__.py.py
@time: 2018-3-2 14:03
"""

#插件
db = SQLAlchemy()

log = flask_logger.Logger()

def create_app():
    app = Flask(__name__)

    #config
    app.config.from_object(config[env])
    config[env].init_app(app)

    #插件注册
    db.init_app(app)
    log.init_app(app,config=config[env].LOG_CONFIG)

    #app注册
    from app.auth import mod_auth
    app.register_blueprint(mod_auth)

    return app
