import json
import requests
from loginCuebLibrary.loginLibrary import login_library
from os import path

parentpath = path.abspath('.')
filepath1 = path.join(parentpath,'info/config.json')
filepath2 = path.join(parentpath,'info/Info.json')

with open(filepath1) as file1:
    config = json.load(file1)

headers = config['headers']
roomIdList = config['roomId']
libraryDeviceUrl = "https://10-21-95-57.webvpn.cueb.edu.cn/ClientWeb/pro/ajax/device.aspx"

def show_seats():

    with open(filepath2) as f2:
        selectionInfo = json.load(f2)

    begin = selectionInfo['start']
    end = selectionInfo['end']
    date = begin.split()[0]
    fr_start = begin.split(" ")[-1]
    fr_end = end.split(" ")[-1]

    try:
        cookies = login_library()
        if (isinstance(cookies,type("str"))):
            yield "登录系统失败，检查用户名，密码"
        else:
            session = requests.Session()
            session.cookies = cookies
            yield cookies
            kv = {
                "byType":"devcls",
                "classkind":"8",
                "display":"fp",
                "md":"d",
                "purpose":"",
                "selectOpenAty":"",
                "cld_name":"default",
                "date":date,
                "fr_start":fr_start,
                "fr_end":fr_end,
                "act":"get_rsv_sta"
            }
            for id in roomIdList:
                kv['room_id'] = id
                resp = session.get(libraryDeviceUrl,headers=headers,params=kv)
                yield resp.text
    except:
        yield "登录系统失败，检查用户名，密码"