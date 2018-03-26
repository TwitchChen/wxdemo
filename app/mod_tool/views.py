# encoding: utf-8

from . import mod_tool
from app.mod_tool.weather import GetWeather
from flask import request

"""
@author: Twitch Chen
@file: views.py
@time: 2018/3/23 下午3:58
"""

gw = GetWeather()

@mod_tool.route("/wxapi/weather")
def weather():
    city = request.args["city"]
    data = gw.get_weather_from_redis(city)
    return data


if __name__ == '__main__':
    print(weather())