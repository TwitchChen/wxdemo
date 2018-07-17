# encoding: utf-8

from . import mod_auth
from app.auth.get_token import GetWxToken
from app import create_app

"""
@author: Twitch Chen
@file: views.py
@time: 2018-3-2 15:02
"""

app = create_app()
token = GetWxToken(app)

@mod_auth.route("/token")
def test():
    t = token.get_token_from_redis()
    return 'ok: %s'%t
