# encoding: utf-8

import os

"""
@author: Twitch Chen
@file: config.py
@time: 2018-3-2 13:59
"""


class Config(object):

    DEBUG = False

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):

    debug = False


class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql://test:Test123456!@192.168.102.167:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #redis
    RED_SERVER = '192.168.102.227'
    RED_PORT = 6379
    RED_DB = 1


    #weixin
    TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
    APPID = 'wx5d865a8fef21ed22' #test id
    APPSECRET = 'fcd0e8efae2f0f3eea1059ab90f01d0d' #test secret
    GRANT_TYPE = 'client_credential'

    #weather
    WEATHRT_ID = '****'
    WEATHER_SECRET = '******'
    BASE_URL = 'https://api.seniverse.com/v3'
    CITY_ID_API = '/location/search.json'

    DEBUG = True


config = {
    "production": ProdConfig,
    "test": TestConfig,
    "default": TestConfig
}

env = 'test'
