import uvicorn as uvicorn
from fastapi import FastAPI
import re
import requests
import json


app = FastAPI()  # 必须实例化该类，启动的时候调用


def get_bilibili_fans_count(uid):

    status_code = 200
    message = "success"
    fanscount = 0

    headers = {"Connection": "close"}
    response = requests.get(f"http://api.bilibili.com/x/web-interface/card?mid={uid}&;jsonp=jsonp&article=true", headers).text
    
    json_response = json.loads(response)
    
    status_code = json_response.get("code")
    message = json_response.get("message")

    if status_code != 0:
        fanscount = -1
        print(message)
    else:
        status_code = 200
        fanscount = json_response.get("data").get("card").get("fans")
        print("bilibili fan number: " + str(fanscount))
    return status_code, fanscount, message


# 请求根目录
@app.get('/')
def index():
    return {'message': '欢迎来到FastApi 服务！'}


@app.get('/api/fanscount/bilibili/uid/{uid}')
def bilibili_fans(uid: str):
    status_code, fanscount, message = get_bilibili_fans_count(uid)
    return {'status' : status_code, "message":message, "data" : { "value" : fanscount}}


if __name__ == '__main__':
    uvicorn.run(app=app, port=40001)