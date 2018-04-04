# encoding: utf-8

from . import mod_tool
from app.mod_tool.weather import GetWeather
from flask import request
from app import create_app

"""
@author: Twitch Chen
@file: views.py
@time: 2018/3/23 下午3:58
"""

app = create_app()
gw = GetWeather(app)

@mod_tool.route("/wxapi/weather")
def weather():
    city = request.args["city"]
    print(city)
    data = gw.get_weather_from_redis(city)
    return "ok: %s" % data

