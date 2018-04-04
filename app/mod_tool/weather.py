# encoding: utf-8

import requests
import json
from app.common.com_redis import Redis

"""
@author: Twitch Chen
@file: weather.py
@time: 2018-3-2 18:34
"""


class GetWeather(object):
    def __init__(self,app):
        self.app = app
        self.redis = Redis(app)
        self.base_url = app.config["BASE_URL"]
        self.id = app.config["WEATHRT_ID"]
        self.key = app.config["WEATHER_SECRET"]
        self.now_url = app.config["NOW_WEATHER"]
        self.three_url = app.config["THREE_DAY_WEATHER"]
        self.shzs_url = app.config["SHZS"]

    def get_city_id(self, city):
        id = ''
        key = "weather_"+city
        id = self.redis.get_from_redis(key=key)
        if id:
            self.app.logger.info("get city id from redis")
            return id
        else:
            request_url = self.app.config["CITY_ID_API"]
            url = self.base_url+request_url
            params = {
                "key": self.key,
                "q": city
            }
            try:
                r = requests.get(url, params, timeout=(5, 5))
                if r.status_code == 200:
                    id = (json.loads(r.text))["results"][0]["id"]
                    self.redis.save_to_redis(key=key, value=id)
                    self.app.logger.info("get city id from api")
                    return id
            except Exception as e:
                self.app.logger.error("get city id error: %s" % e)
                return None

    def get_weather_from_redis(self, city):
        if not city:
            self.app.logger.info("test 1")
            return None
        key = "weather_"+city
        data = self.redis.get_from_redis(key=key)
        if data:
            self.app.logger.info("test 2")
            return data
        else:
            data = self.get_weather_from_api(city)
            self.redis.save_to_redis(key=key, value=data, ex=3600)
            self.app.logger.info("test 3")
            return data

    def get_weather_from_api(self, city):
        now = self.base_url + self.now_url
        three = self.base_url + self.three_url
        sh = self.base_url + self.shzs_url
        urls = {
            "now": now,
            "three": three,
            "sh": sh
        }
        data = {}
        now_data = {}
        three_data = {}
        sh_data = {}
        params = {
            "key": self.key,
            "location": city
        }
        for url in urls.keys():
            try:
                r = requests.get(url=urls[url], params=params)
                self.app.logger.info("url debug: %s" %urls[url])
                if r.status_code == 200:
                    d = json.loads(r.text)
                    self.app.logger.info("test 4")
                    if d["results"]:
                        data[url] = d["results"][0]
                    else:
                        data[url] = ""
                else:
                    self.app.logger.error("get weather error, %s" % r.status_code)
                    continue
            except Exception as e:
                self.app.logger.error("%s warther api error, %s" %(url, e))
                continue
        if data["now"]:
            now_data["name"] = data["now"]["location"]["name"]
            now_data["path"] = data["now"]["location"]["path"]
            now_data["status"] = data["now"]["now"]["text"]
            now_data["temperature"] = data["now"]["now"]["temperature"]
        if data["three"]:
            for day in data["three"]["daily"]:
                pass
        return now_data


