# encoding: utf-8

from app import create_app
from .robot import Robot
from . import mod_robot

"""
@author: Twitch Chen
@file: views.py
@time: 2018/6/29 下午3:32
"""

app = create_app()
robot = Robot(app)

@mod_robot.route('/robot/text', methods = ['GET', 'POST'])
def get_text():
    print(robot.get_text("hello",'sdfsafsa'))
    return 'ok'