# encoding: utf-8

import requests,json


"""
@author: Twitch Chen
@file: robot.py
@time: 2018/6/29 下午2:56
"""

class Robot(object):

    def __init__(self, app):
        self.url = app.config['ROBOT_URL']
        self.apikey = app.config['ROBOT_APIKEY']
        self.app = app

    def get_text(self,text,user):
        data = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": text
                }
            },
            "userInfo": {
                "apiKey": self.apikey,
                "userId": user
            }
        }
        rsp = {}
        try:
            r = requests.post(url=self.url, data=json.dumps(data), timeout=(2,5))
            if r.status_code == 200:
                t = json.loads(r.text)
                code = t['intent']['code']
                if code in [5000,6000,4000,4001,4002,4003,4005,4007,4100,4200,4300,4400,4500,5600,4602,7002,8008]:
                    rsp['code'] = 400
                    rsp['msg'] = t['intent']['results'][0]['values']['text']
                    rsp['value'] = ''
                    self.app.logger.error("获取图灵机器人接口数据错误,user:%s,code:%s,msg:%s"%(user,code, rsp['msg']))
                else:
                    rsp['code'] = 200
                    rsp['msg'] = 'success'
                    rsp['value'] = t['intent']['results'][0]['values']['text']
                    self.app.logger.info("调用图灵机器人接口成功,user:%s,code:%s,msg:%s" % (user,code, rsp['msg']))
            else:
                rsp['code'] = r.status_code
                rsp['msg'] = 'url error'
                rsp['value'] = ''
                self.app.logger.error("调用图灵机器人接口错误,user:%s,code:%s,msg:%s" % (user, r.status_code, rsp['msg']))
        except Exception as e:
            rsp['code'] = 400
            rsp['msg'] = e
            rsp['value'] = ''
            self.app.logger.error("调用图灵机器人接口错误,user:%s,code:%s,msg:%s" % (user, 500, rsp['msg']))

        return rsp


