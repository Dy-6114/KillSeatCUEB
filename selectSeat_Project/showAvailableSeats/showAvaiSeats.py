import json
import time
import datetime
from showSeats.showAllseats import show_seats
from os import path

parentpath = path.abspath('.')
filepath1 = path.join(parentpath,'info/config.json')
filepath2 = path.join(parentpath,'info/Info.json')
filepath3 = path.join(parentpath,'info/bestSeats.json')

with open(filepath1) as f:
    config = json.load(f)

with open(filepath3) as f1:
    bestSeatsInfo = json.load(f1)

def show_available_seat():

    global cookies, newBegin, devId, newEnd, roomName, devName, className, freeTime

    with open(filepath2) as f2:
        selectionInfo = json.load(f2)

    startSec = time.mktime(time.strptime(selectionInfo['start'], "%Y-%m-%d %H:%M"))
    now = (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M")
    nowSec = time.mktime(time.strptime(now, "%Y-%m-%d %H:%M"))
    if (startSec > nowSec):
        begin = selectionInfo['start']
    else:
        begin = now
    end = selectionInfo['end']
    generator = show_seats()
    cookies = next(generator)
    if (isinstance(cookies,type("str"))):
        return "登录系统失败，检查用户名，密码"
    else:
        pass
    notFullTimeSeats = []
    fullTimeSeats = []

    for Seats in generator:
        seats = json.loads(Seats)
        for seat in seats['data']:
            if (seat['state'] != "close"):
                if (seat['ts']):
                    notFullTimeSeats.append(seat)
                else:
                    fullTimeSeats.append(seat)
            else:
                pass

    if (len(fullTimeSeats)!=0): #如果有符合要求的座位
        for str in fullTimeSeats:
            if (str['devId'] in bestSeatsInfo['seatId']): #返回众多符合要求座位中的较好的双人座位中的一个
                devId = str['devId']
                roomName = str['roomName']
                devName = str['devName']
                className = str['className']
                freeTime = str['freeTime']
                break
            else:
                continue
        if (devId):
            pass
        else:#返回一般的座位
            devId = fullTimeSeats[0]['devId']
            roomName = fullTimeSeats[0]['roomName']
            devName = fullTimeSeats[0]['devName']
            className = fullTimeSeats[0]['className']
            freeTime = fullTimeSeats[0]['freeTime']
        newBegin = begin
        newEnd = end
    else:
        seatStart = notFullTimeSeats[0]['ts'][0]['start']
        dateStartSec = time.mktime(time.strptime(seatStart, "%Y-%m-%d %H:%M"))
        beginSec = time.mktime(time.strptime(begin, "%Y-%m-%d %H:%M"))
        lastTime = dateStartSec-beginSec
        index = 0
        for i in range(len(notFullTimeSeats)):
            seatStart1 = notFullTimeSeats[i]['ts'][0]['start']
            dateStartSec1 = time.mktime(time.strptime(seatStart1, "%Y-%m-%d %H:%M"))
            if ((dateStartSec1-beginSec)>lastTime):
                lastTime = dateStartSec1-beginSec
                index = i
            else:
                continue
        if (lastTime>0):
            devId = notFullTimeSeats[index]['devID']
            roomName = notFullTimeSeats[index]['roomName']
            devName = notFullTimeSeats[index]['devName']
            className = notFullTimeSeats[index]['className']
            freeTime = lastTime
            newEnd = notFullTimeSeats[index]['ts'][0]['start']
            newBegin = begin
        else:
            print("对不起，没有找到适合你的座位。")
    return cookies,devId,newBegin,newEnd,roomName,devName,className,freeTime