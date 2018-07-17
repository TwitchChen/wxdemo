# encoding: utf-8

from flask import Flask
from config_loc import config,env
from flask_sqlalchemy import SQLAlchemy
import logging

"""
@author: Twitch Chen
@file: __init__.py.py
@time: 2018-3-2 14:03
"""

#插件
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    #config
    app.config.from_object(config[env])
    config[env].init_app(app)

    #插件注册
    db.init_app(app)

    #log
    handler = logging.FileHandler(config[env].LOG_PATH, encoding='UTF-8')
    handler.setLevel(config[env].LOG_LEVEL)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    #app注册
    #认证模块
    from app.auth import mod_auth
    app.register_blueprint(mod_auth)
    #小工具
    from app.mod_tool import mod_tool
    app.register_blueprint(mod_tool)
    #robot
    from app.robot import mod_robot
    app.register_blueprint(mod_robot)
    #wx
    from app.wx_api import mod_wx
    app.register_blueprint(mod_wx)

    return app
