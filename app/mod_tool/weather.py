# encoding: utf-8

import requests
import json
from app import create_app
from app.common.com_redis import Redis



"""
@author: Twitch Chen
@file: weather.py
@time: 2018-3-2 18:34
"""

app = create_app()


class GetWeather(object):
    def __init__(self):
        self.base_url = app.config["BASE_URL"]
        self.id = app.config["WEATHRT_ID"]
        self.key = app.config["WEATHER_SECRET"]
        self.now_url = app.config["NOW_WEATHER"]
        self.three_url = app.config["THREE_DAY_WEATHER"]
        self.shzs_url = app.config["SHZS"]
        self.redis = Redis()

    def get_city_id(self, city):
        id = ''
        id = self.redis.get_from_redis(key=city)
        if id:
            return id
        else:
            request_url = app.config["CITY_ID_API"]
            url = self.base_url+request_url
            params = {
                "key": self.key,
                "q": city
            }
            try:
                r = requests.get(url, params, timeout=(5, 5))
                if r.status_code == 200:
                    id = (json.loads(r.text))["results"][0]["id"]
                    self.redis.save_to_redis(key=city, value=id)
                    return id
            except Exception as e:
                app.logger.error("get city id error: %s" % e)
                return None

    def get_weather_from_redis(self, city):
        if not city:
            return None
        key = "weather_"+city
        data = self.redis.get_from_redis(key=key)
        if data:
            return data
        else:
            data = self.get_weather_from_api(city)
            self.redis.save_to_redis(key=city, value=data)
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
        params = {
            "key": self.key,
            "q": city
        }
        for url in urls.keys():
            try:
                r = requests.get(url=urls[url], params=params)
                if r.status_code == 200:
                    d = json.loads(r.text)
                    data[url] = d["results"][0][url]
                else:
                    app.logger.error("get weather error, %s" % r.status_code)
                    continue
            except Exception as e:
                app.logger.error("%s warther api error, %s" %(url, e))
                continue
        return data


