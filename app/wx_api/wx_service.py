# encoding: utf-8

import requests
import json
from app.common.com_redis import Redis
from .WXBizMsgCrypt import XMLParse, WXBizMsgCrypt, Prpcrypt

"""
@author: Twitch Chen
@file: wx_service.py
@time: 2018/7/12 下午4:07
"""

class GetWxToken(object):

    def __init__(self, app):
        """
        获取微信api的token,并存入redis
        :param app:
        """
        self.token_url = app.config["TOKEN_URL"]
        self.appID = app.config["APPID"]
        self.appsecret = app.config["APPSECRET"]
        self.grant_type = app.config["GRANT_TYPE"]
        self.redis = Redis(app)
        self.app = app

    def save_token_to_redis(self):
        params = {
            "appID": self.appID,
            "secret": self.appsecret,
            "grant_type": self.grant_type
        }
        try:
            r = requests.get(url=self.token_url, params=params)
            if r.status_code == 200:
                token = json.loads(r.text)['access_token']
                ex = json.loads(r.text)['expires_in']
                self.redis.save_to_redis(key='wx_token', value=token, ex=ex)
                return token
            else:
                return None
        except Exception as e:
            self.app.logger.error("get wx token error: {}".format(e))
            return None

    def get_token_from_redis(self):
        key = "wx_token"
        token = ''
        try:
            token = self.redis.get_from_redis(key=key)
        except Exception as e:
            self.app.logger.error("redis error,{}".format(e))
        if token:
            self.app.logger.info("get token from redis")
            return token
        else:
            self.app.logger.info("get token from wx")
            return self.save_token_to_redis()

class WxApi(object):
    def __init__(self,app):
        self.app = app

    def get_wx_data(self,args,body):
        """
        获取微信参数及post body
        :param app:
        :return:参数及
        """
        token = self.app.config['MSG_TOKEN']
        sEncodingAESKey = self.app.config['ENCODINGAESKEY']
        sAppId = self.app.config['APPID']
        signature  = ''
        timestamp = ''
        nonce = ''
        openid = ''
        encrypt_type = ''
        msg_signature = ''
        try:
            signature = args['signature'] if args['signature'] else ''
            timestamp = args['timestamp'] if args['timestamp'] else ''
            nonce = args['nonce'] if args['nonce'] else ''
            openid = args['openid'] if args['openid'] else ''
            encrypt_type = args['encrypt_type'] if args['encrypt_type'] else ''
            msg_signature = args['msg_signature'] if args['msg_signature'] else ''
        except Exception as e:
            self.app.logger.error('get wx args error, {}'.format(e))
            return None
        msgcrype = WXBizMsgCrypt(sToken=token, sEncodingAESKey=self.app.config['ENCODINGAESKEY'], sAppId=self.app.config['APPID'],app=self.app)
        ret,decryp_xml = msgcrype.DecryptMsg(sPostData=body,sMsgSignature=msg_signature,sTimeStamp=timestamp,sNonce=nonce)
        return decryp_xml if decryp_xml else ''

    def on_text(self):
        """
        回复wx的文本消息
        :return:
        """
        to_xml = """<xml>\n
        <ToUserName><![CDATA[%s]]></ToUserName>\n
        <FromUserName><![CDATA[%s]]></FromUserName>\n
        <CreateTime>%s</CreateTime>\n
        <MsgType><![CDATA[text]]></MsgType>\n
        <Content><![CDATA[%s]]></Content>\n
        <MsgId><![CDATA[%s]]></MsgId>\n
        </xml>"""
        pass



