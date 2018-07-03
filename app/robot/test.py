# encoding: utf-8

import requests,json

"""
@author: Twitch Chen
@file: test.py
@time: 2018/6/29 下午2:21
"""

url = 'http://openapi.tuling123.com/openapi/api/v2'
apikey = '92fdb416709b46ada0989e9a105e5476'


data = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": "股票"
        }
    },
    "userInfo": {
        "apiKey": apikey,
        "userId": ""
    }
}
r = requests.post(url=url,data=json.dumps(data))
t = json.loads(r.text)
print(r.text)
code = t['intent']['code']
if code in [5000, 6000, 4000, 4001, 4002, 4003, 4005, 4007, 4100, 4200, 4300, 4400, 4500, 5600, 4602, 7002, 8008]:
    print("error")
else:
    print("ok")