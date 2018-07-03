# encoding: utf-8

from flask import Blueprint

"""
@author: Twitch Chen
@file: __init__.py.py
@time: 2018/6/29 下午2:21
"""

mod_robot = Blueprint("mod_robot", __name__)


from . import views