from django.shortcuts import render
from django.http import HttpResponse
from os.path import dirname, abspath
import mmap
from django_eventstream import send_event


def output(request,filename):
    # file = dirname(dirname(dirname(dirname(abspath(__file__))))) + '/console-server/20005.log'
    file = dirname(dirname(dirname(dirname(abspath(__file__))))) + '/console-server/' + filename +'.log'
    with open(file,'rb+') as f:
        try:
            memfile = mmap.mmap(f.fileno(),0)
            msg = memfile.read()
            print(msg)
        except Exception as e:
            print(Exception,e)
            memfile.close()
        else:
            memfile.seek(0)

    #r = HttpResponse("<pre>" + msg + "</pre>",content_type="text/event-stream")
    r = HttpResponse(msg,content_type="text/event-stream")
    print(r)
    return r

    #send_event('test', 'message', {'text': 'aaaaaaaaaa'})
'''
import time
from django.http import StreamingHttpResponse
from django.utils.timezone import now
import telnetlib
from telnetlib import IAC,NOP
import logging
import pdb

#打开一个telnet连接并keepalive
def console_conn(HOST='192.168.2.201',PORT='20015'):
    try:
        tn = telnetlib.Telnet(host=HOST,port=PORT)
        tn.set_debuglevel(2)
    except Exception as e:
        print('******** some error happened  *********')
        print(Exception,":",e)
    if tn.sock.sendall(IAC + NOP):   #发送空操作keepalive
        pass
    return tn

#读取telnet信息写入txt
def read_msg(tn=console_conn()):
    msg = tn.read_eager()
    return msg

def msg_format(msg):
    if type(msg) == str:
        txt = msg.split("\r\n")
        for i in txt:
            print(i)
    elif type(msg) == bytes:
        msg = msg.decode('ascii')
        msg_format(msg)
    else:
        print('*** 锟斤拷 ：msg_format***')
        # traceback.print_exc()
        # raise
    return msg

def eventsource(request):
    response = StreamingHttpResponse(stream_generator(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response

def stream_generator():
    global tmptime
    tmptime = nowTime
    while True:
        msg = read_msg()
        if msg == b'':
            pass
        else:
            msg = msg_format(msg)

            if tmptime == nowTime:
                yield msg
            else:
                yield tmptime + msg
                global tmptime
                tmptime = nowTime
        # time.sleep(2)

nowTime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
'''