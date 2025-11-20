import json
import re
import requests
from os import path
from loginCuebPlatform.loginPlatform import login_platform

libraryTempUrl = "https://mh.webvpn.cueb.edu.cn/portal/home/resource?id=5b60c71467366e4801673e7dbe1c0051" #学校图书馆的id固定，所以不做params处理，直接get
libraryDefaultUrl = "https://10-21-95-57.webvpn.cueb.edu.cn/ClientWeb/xcus/ic2/Default.aspx"
libraryLoginUrl = "https://10-21-95-57.webvpn.cueb.edu.cn/ClientWeb/pro/ajax/login.aspx"


parentpath = path.abspath('.')
filepath1 = path.join(parentpath,'info/config.json')
filepath2 = path.join(parentpath,'info/Info.json')

with open(filepath1) as f1:
    config = json.load(f1)

headers = config['headers']

def login_library():
    with open(filepath2) as f2:
        selectionInfo = json.load(f2)

    try:
        cookies = login_platform()

        session = requests.Session()
        session.cookies = cookies

        r1 = session.get(libraryTempUrl,headers=headers)
        library_token = re.search(r'token=.*\'',r1.text).group(0).strip("'").split('=')[-1] #获取图书馆token
        r2 = session.get(libraryDefaultUrl,params={'token':library_token},headers=headers)
        data = {
            'id':selectionInfo['student']['user'],
            'pwd':selectionInfo['student']['librarypwd'],
            'act':'login'
        }
        r3 = session.post(libraryLoginUrl,data=data,headers=headers)
        return session.cookies
    except:
        return "登录失败，检查用户名，密码。"
