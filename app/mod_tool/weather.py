# encoding: utf-8

import requests
import json
from app import create_app

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

    def get_city_id(self, city):
        request_url = app.config["CITY_ID_API"]
        url = self.base_url+request_url
        params = {
            "key": self.key,
            "q": city
        }
        try:
            r = requests.get(url, params, timeout=(5, 5))
            if r.status_code == 200:
                return "ok"
        except Exception as e:
            return "error", e

    def get_weather(self):
        pass

