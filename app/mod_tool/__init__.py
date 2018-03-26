# encoding: utf-8

from flask import Blueprint

"""
@author: Twitch Chen
@file: __init__.py.py
@time: 2018-3-1 16:14
"""

mod_tool = Blueprint("mod_tool", __name__)


from . import views