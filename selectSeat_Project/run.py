import json
from tkinter import *
import tkinter
import datetime
from selectSeat.selection import select_seat
from delSelectSeat.delRsv import del_rsv
from os import path

time = datetime.datetime.now() + datetime.timedelta(minutes=20)
now = time.strftime("%Y-%m-%d %H:%M")
end = time.strftime("%Y-%m-%d") + " 23:00"

class cuebAssitant():

    def __init__(self):
        self.parentpath = path.abspath('.')
        self.filepath = path.join(self.parentpath, 'info/Info.json')
        self.root = Tk()
        self.root.title("首都经济贸易大学图书馆约座助手v2.0")
        self.root.geometry('500x400')
        self.caution1 = Label(self.root,text="默认Sjm+身份证后六位",width='25',height='3')
        self.caution2 = Label(self.root, text="默认为学号", width='25', height='3')
        self.caution3 = Label(self.root, text="格式：2001-01-18 09:31", width='25', height='3')
        self.idlabel = Label(self.root,text="个人学号：",width='25',height='3')
        self.pwdlabel = Label(self.root,text="上网密码：",width='25',height='3')
        self.librarypwdlabel = Label(self.root,text="约座系统密码：",width='25',height='3')
        self.nowlabel = Label(self.root,text="预约开始时间：",width='25',height='3')
        self.endlabel = Label(self.root,text="预约结束时间：",width='25',height='3')
        self.idtext = Entry(self.root,width='20')
        self.pwdtext = Entry(self.root,width='20')
        self.librarypwdtext = Entry(self.root,width='20')
        self.nowtext = Entry(self.root,width='20')
        self.endtext = Entry(self.root,width='20')
        self.rsvbutton = Button(self.root, text="点击快速预约", width='10',command=lambda: self.commit())
        self.delrsvbutton = Button(self.root, text="点击取消预约", width='10', command=lambda: self.delRsv())
        self.commitText = Label(self.root,text='')

    def arrange(self):
        self.idlabel.grid(row=0,column=0)
        self.idtext.grid(row=0,column=1)
        self.pwdlabel.grid(row=1,column=0)
        self.pwdtext.grid(row=1,column=1)
        self.caution1.grid(row=1, column=2)
        self.librarypwdlabel.grid(row=2,column=0)
        self.librarypwdtext.grid(row=2,column=1)
        self.caution2.grid(row=2, column=2)
        self.nowlabel.grid(row=3,column=0)
        self.nowtext.grid(row=3,column=1)
        self.nowtext.insert(0,now)
        self.caution3.grid(row=3, column=2)
        self.endlabel.grid(row=4,column=0)
        self.endtext.grid(row=4,column=1)
        self.endtext.insert(0,end)
        self.rsvbutton.grid(row=5,column=0)
        self.delrsvbutton.grid(row=5,column=1)
        self.commitText.grid(row=8,columnspan=3)

    def commit(self):
        begin = self.nowtext.get()
        finish = self.endtext.get()
        user = self.idtext.get()
        pwd = self.pwdtext.get()
        lbpwd = self.librarypwdtext.get()
        dic = {
            "student": {
                "user": user,
                "pwd": pwd,
                 "librarypwd": lbpwd
            },
            "start": begin,
            "end": finish
            }
        with open(self.filepath,"w",encoding='utf8') as f:
            json.dump(dic, f)
        if (len(begin) != 0 and len(finish) != 0 and len(user) != 0 and len(pwd) != 0 and len(lbpwd) != 0):
            content = select_seat()
            self.commitText['text'] = content
        else:
            self.commitText['text'] = "所有输入框不能为空"

    def delRsv(self):
        content = []
        generator = del_rsv()
        for str in generator:
            dic = json.loads(str)
            content.append(dic['msg'])
        self.commitText['text'] = content

tk = cuebAssitant()
tk.arrange()
tkinter.mainloop()

