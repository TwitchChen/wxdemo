# encoding: utf-8

import requests
import json
from app import create_app
from app.common.com_redis import Redis

"""
@author: Twitch Chen
@file: get_token.py
@time: 2018-3-1 16:14
"""

app = create_app()

redis = Redis()


class GetWxToken(object):

    def __init__(self):
        self.token_url = app.config["TOKEN_URL"]
        self.appID = app.config["APPID"]
        self.appsecret = app.config["APPSECRET"]
        self.grant_type = app.config["GRANT_TYPE"]

    def save_token_to_redis(self):
        params = {
            "appID": self.appID,
            "secret": self.appsecret,
            "grant_type": self.grant_type
        }
        try:
            r = requests.get(url=self.token_url, params=params)
            if r.status_code == 200:
                token = json.loads(r.text)['access_token']
                ex = json.loads(r.text)['expires_in']
                redis.save_to_redis(key='wx_token', value=token, ex=ex)
                return token
            else:
                return None
        except Exception as e:
            app.logger.error("get wx token error: %s" % e)
            #print("error log")
            return None

    def get_token_from_redis(self):
        key = "wx_token"
        token = redis.get_from_redis(key=key)
        if token:
            app.logger.info("get token from redis")
            return token
        else:
            app.logger.info("get token from wx")
            return self.save_token_to_redis()

