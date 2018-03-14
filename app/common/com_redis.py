# encoding: utf-8

import redis
from app import create_app

"""
@author: Twitch Chen
@file: com_redis.py
@time: 2018-3-1 16:44
"""

app = create_app()
server = app.config["RED_SERVER"]
port = app.config["RED_PORT"]
db = app.config["RED_DB"]


class Redis(object):
    def __init__(self):
        self.conn = redis.Redis(host=server, port=port, db=db)

    def save_to_redis(self, key=None, value=None, ex=None):
        try:
            r = self.conn.set(name=key, value=value,ex=ex)
            if r:
                return True
            else:
                print("redis error")
                return False
        except Exception as e:
            print("log error: %s" % e)
            return False

    def get_from_redis(self, key):
        try:
            r = self.conn.get(name=key)
            if r:
                return r
            else:
                print("redis error")
                return None
        except Exception as e:
            print("log error %s" % e)
            return None


