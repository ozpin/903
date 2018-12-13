# --*--code:utf-8--
# !/usr/bin/enc python3
# 建立一个telnet连接，什么也不send，就连接

import telnetlib
from telnetlib import IAC,NOP
import time
import traceback
import sys
import time
import os
import signal
import selectors
#selectors模块默认会用epoll，如果你的系统中没有epoll(比如windows)则会自动使用select

#迭代器
def yld(sta,num):
    u=sta
    while u <= num :
        yield u
        u+=1

def read_msg(tn,mask):
    try:
        msg = tn.read_eager()
        with open(str(tn.host) + "_" + str(tn.port) + ".log", "a") as f:
            f.write(msg.decode('ascii'))
        print("msg length : ",len(msg.decode('ascii')))
    except Exception as e:
        sel.unregister(tn)
        tn.close()
        print('*** 烫烫烫 : read_msg***')




tn = telnetlib.Telnet()
tn.set_debuglevel(2)

sel  = selectors.DefaultSelector()   #生成一个select对象

for port in yld(10003, 10003):
    server_200 = "192.168.2.200"
    tn = tn.open(server_200,port)
    try:
        print("into selectors")
        sel.register(tn, selectors.EVENT_READ , read_msg)
    except Exception as e:
        break

while True:
    try:
        print("into events")
        events = sel.select()      #默认是阻塞，有活动连接就返回活动的连接列表
        print(events)
        for key,mask in events:
            print("key",key)
            callback = key.data
            print(callback)
            callback(key.fileobj, mask)
    except KeyboardInterrupt:
        print("Ctrl ^C")
        print("Exception : Warning!Warning!")
        print("人工退出完毕")
        tn.close()
        sel.close()
        break

'''
备用代码
nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

#打开一个telnet连接

        #sel.register(tn,selectors.EVENT_READ | selectors.EVENT_WRITE,)
        if tn.sock.sendall(IAC + NOP):  # 发送空操作keepalive
            pass
    except Exception as e:
        print('******** some error happened  *********')
        print(Exception,":",e)
    return tn

#递归实现根据\r\n进行分割然后格式化输出信息
def msg_format(msg):
    if type(msg) == str:
        txt = msg.split("\r\n")
        for i in txt:
            print(i)
    elif type(msg) == bytes:
        msg = msg.decode('utf-8')
        msg_format(msg)
    else:
        print('*** 锟斤拷 ：msg_format***')
        # traceback.print_exc()
        # raise
'''