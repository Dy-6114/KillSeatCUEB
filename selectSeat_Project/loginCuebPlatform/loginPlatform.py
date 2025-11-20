import base64
import re
import json
import requests
from bs4 import BeautifulSoup
from os import path

parentpath = path.abspath('.')
filepath1 = path.join(parentpath,'info/config.json')
filepath2 = path.join(parentpath,'info/Info.json')

vpnLoginUrl = "https://webvpn.cueb.edu.cn/users/sign_in" #vpn登录页面
sjmLoginUrl_jsessionid = "https://cas-443.webvpn.cueb.edu.cn/sso/login?appId=portal" #获取jsessionid
sjmLoginUrl_castgc = "https://cas-443.webvpn.cueb.edu.cn/sso/login" #获取castgc和token
sjmLoginUrl = "https://mh.webvpn.cueb.edu.cn/portal/home" #首经贸综合信息平台页面

with open(filepath1) as f1:
    config = json.load(f1)

headers = config['headers']

def login_platform():
    with open(filepath2) as f2:
        selectionInfo = json.load(f2)

    base64_user = base64.b64encode(selectionInfo['student']['user'].encode()).decode()
    base64_pwd = base64.b64encode(selectionInfo['student']['pwd'].encode()).decode()
    session = requests.Session()

    r1 = session.get(vpnLoginUrl,headers=headers)
    auth_token = re.search(r'<meta name="csrf-token" content=".*?" />',r1.text).group(0).split('"')[-2] #获取认证token
    data = {
        'utf8': '✓',
        'authenticity_token': auth_token,
        'user[login]': selectionInfo['student']['user'],
        'user[password]': selectionInfo['student']['pwd'],
        'user[dymatice_code]': 'unknown',
        'commit': '登录 Login'

    }
    r2 = session.post(vpnLoginUrl,data=data,headers=headers)
    r3 = session.get(sjmLoginUrl_jsessionid)
    soup = BeautifulSoup(r3.text,'html.parser')
    loginTicket = soup.form.find('input',attrs={'id':"loginTicket"}).attrs['value'] #获取loginTicket
    data2 = {
        'loginTicket':loginTicket,
        'username':base64_user,
        'appId':'portal',
        'password':base64_pwd
    }
    r4 = session.post(sjmLoginUrl_castgc,data=data2,headers=headers)
    platform_token = re.search(r'token=.*?&',r4.text).group(0).strip("&").split("=")[-1] #获取平台登录token
    kv = {
        'token':platform_token,
        'params':''
    }
    r5 = session.get(sjmLoginUrl,headers=headers,params=kv) #登录综合信息平台
    return session.cookies

print(login_platform())