import json
import re
from os import path

import requests
from loginCuebLibrary.loginLibrary import login_library

parentpath = path.abspath('.')
filepath = path.join(parentpath,'info/config.json')

with open(filepath) as f:
    config = json.load(f)


headers = config['headers']

seatDelUrl = "https://10-21-95-57.webvpn.cueb.edu.cn/ClientWeb/pro/ajax/reserve.aspx"
libraryCenterUrl = "https://10-21-95-57.webvpn.cueb.edu.cn/ClientWeb/pro/ajax/center.aspx?act=get_History_resv&strat=90&StatFlag=New"

def del_rsv():
    cookies = login_library()
    session = requests.session()
    session.cookies = cookies
    r1 = session.get(libraryCenterUrl)
    html = r1.text
    rsvIdList = re.findall(r'rsvId=\'\d*\'',html)
    for str in rsvIdList:
        rsvId = str.split('=')[-1].strip("'")
        kv = {
            "act":"del_resv",
            "id":rsvId,
        }
        resp = session.get(seatDelUrl,headers=headers,params=kv)
        yield resp.text