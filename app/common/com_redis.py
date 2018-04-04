# encoding: utf-8

import redis


"""
@author: Twitch Chen
@file: com_redis.py
@time: 2018-3-1 16:44
"""


class Redis(object):
    def __init__(self, app):
        self.server = app.config["RED_SERVER"]
        self.port = app.config["RED_PORT"]
        self.db = app.config["RED_DB"]
        self.conn = redis.Redis(host=self.server, port=self.port, db=self.db)
        self.app = app

    def save_to_redis(self, key=None, value=None, ex=None):
        try:
            r = self.conn.set(name=key, value=value,ex=ex)
            if r:
                return True
            else:
                self.app.logger.error("redis error,set  key error")
               # print("redis error")
                return False
        except Exception as e:
            self.app.logger.error("redis connect error: %s" % e)
           # print("log error: %s" % e)
            return False

    def get_from_redis(self, key):
        try:
            r = self.conn.get(name=key)
            if r:
                return r
            else:
                self.app.logger.error("get redis  key error")
                #print("redis error")
                return None
        except Exception as e:
            self.app.logger.error("redis connect error: %s" % e)
            #print("log error %s" % e)
            return None


