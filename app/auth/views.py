# encoding: utf-8


from . import mod_auth
from app.auth.get_token import GetWxToken
from flask import current_app

"""
@author: Twitch Chen
@file: views.py
@time: 2018-3-2 15:02
"""

token = GetWxToken()


@mod_auth.route("/")
def test():
    t = token.get_token_from_redis()

    return t
