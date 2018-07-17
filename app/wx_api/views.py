# encoding: utf-8

from app import create_app
from . import mod_wx
from flask import request, make_response
from .WXBizMsgCrypt import XMLParse, WXBizMsgCrypt, Prpcrypt
from app.robot.robot import Robot
import time

app = create_app()
dxml = XMLParse(app=app)
rob = Robot(app=app)

"""
@author: Twitch Chen
@file: views.py
@time: 2018/7/3 下午4:05
"""

@mod_wx.route("/wx", methods = ["GET", "POST"])
def index():
    if request.method == 'GET':
        return request.args['echostr']
    else:
        token = app.config['MSG_TOKEN']
        xmltext = request.stream.read()
        signature = request.args['signature'] if request.args['signature'] else ''
        timestamp = request.args['timestamp'] if request.args['timestamp'] else ''
        nonce = request.args['nonce'] if request.args['nonce'] else ''
        openid = request.args['openid'] if request.args['openid'] else ''
        encrypt_type = request.args['encrypt_type'] if request.args['encrypt_type'] else ''
        msg_signature = request.args['msg_signature'] if request.args['msg_signature'] else ''

        msgcrype = WXBizMsgCrypt(sToken=token, sEncodingAESKey=app.config['ENCODINGAESKEY'], sAppId=app.config['APPID'],app=app)
        ret,decryp_xml = msgcrype.DecryptMsg(sPostData=xmltext,sMsgSignature=msg_signature,sTimeStamp=timestamp,sNonce=nonce)
        touser_name,fromuser_name, msg_type, content, msg_id = dxml.extract_get_msg(decryp_xml)
        i = ''
        userid = ''
        for i in touser_name.split('_'):
            userid = userid + i

        rob_data = rob.get_text(text=content, user=userid)
        if rob_data['code'] == 200:
            send_content = rob_data['value']
        else:
            send_content = ""
        to_xml = """<xml>\n
        <ToUserName><![CDATA[%s]]></ToUserName>\n
        <FromUserName><![CDATA[%s]]></FromUserName>\n
        <CreateTime>%s</CreateTime>\n
        <MsgType><![CDATA[text]]></MsgType>\n
        <Content><![CDATA[%s]]></Content>\n
        <MsgId><![CDATA[%s]]></MsgId>\n
        </xml>"""


        resp_xml = to_xml %(fromuser_name,touser_name,timestamp,send_content,msg_id)
        ret, encryp_xml = msgcrype.EncryptMsg(sReplyMsg=resp_xml,sNonce=nonce,timestamp=timestamp)
        response = make_response(encryp_xml)
        response.content_type = 'text/xml'



        return response