import json
from showAvailableSeats.showAvaiSeats import show_available_seat
import requests
from os import path

parentpath = path.abspath('.')
filepath1 = path.join(parentpath,'info/config.json')
with open(filepath1) as f:
    config = json.load(f)

seatReserveUrl = "https://10-21-95-57.webvpn.cueb.edu.cn/ClientWeb/pro/ajax/reserve.aspx"

def select_seat():
    tuple = show_available_seat()
    if(isinstance(tuple[0],type('str'))):
        return "登录系统失败，检查用户名，密码"
    else:
        cookies, devId, newBegin, newEnd, roomName, devName, className, freeTime = tuple
        headers = config['headers']
        begin = newBegin
        end = newEnd
        startTime = begin.split()[-1].split(':')[0] + begin.split()[-1].split(':')[1]
        endTime = end.split()[-1].split(':')[0] + end.split()[-1].split(':')[1]

        try:
            session = requests.Session()
            session.cookies = cookies
            kv = {
                'dialogid': '',
                'dev_id': devId,
                'lab_id': '',
                'kind_id': '',
                'room_id': '',
                'type': 'dev',
                'prop': '',
                'test_id': '',
                'term': '',
                'number': '',
                'classkind': '',
                'test_name': '',
                'start': begin,
                'end': end,
                'start_time': startTime,
                'end_time': endTime,
                'up_file': '',
                'memo': '',
                'act': 'set_resv',
            }
            r1 = session.get(seatReserveUrl, headers=headers, params=kv)
            content = json.loads(r1.text)
            if (content['ret'] == 1):
                return ("恭喜你成功预约到了{}的{}{}，预约时长为：{}分钟。".format(roomName, devName, className,freeTime))
            else:
                return content + "\n很遗憾预约座位失败，看看msg的原因，实在不行，去手动约座吧。。"
        except:
            return "请仔细检查输入的所有信息，如果没有问题那就是我的问题，那就手动约座吧。"