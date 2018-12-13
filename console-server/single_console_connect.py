# --*--code:utf-8--
# !/usr/bin/enc python3
# 建立一个telnet连接，什么也不send，就连接

import telnetlib
from telnetlib import IAC,NOP
import mmap
import logging
import pdb


#迭代器
def yld(sta,num):
    u=sta
    while u <= num :
        yield u
        u+=1

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
    return msg


#打开一个telnet连接并keepalive
def console_conn(HOST,PORT):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
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
def read_msg(tn):
    msg = tn.read_eager()
    # print(msg)
    # pdb.set_trace()
    try:
        with open(str(tn.port) + ".log", "a") as f:
            mm = mmap.mmap(f.fileno(),0)
            mm.write(msg.decode('ascii'))
            mm.flush()
        #print("*** 烫烫烫 : read_msg***")
        #msg_format(msg)
    except Exception as e:
        print('*** 烫烫烫 : read_msg***')
        #print(tn.read_all().decode('ascii'))
        #print(msg_format(tn.read_all().decode('ascii')))




'''
备用代码
nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
'''

#sel  = selectors.DefaultSelector()   #生成一个select对象
# HOST = "192.168.2.200"
# PORT = "10005"

#生成一堆socket
for num in yld(10012, 10012):
    server_200 = "192.168.2.200"
    port = num
    tn = console_conn(server_200,port)
    # try:
    #     sel.register(tn, selectors.EVENT_READ, read_msg)
    # except Exception as e:
    #     break

with open(str(tn.port) + ".log", "ab+") as f:
    f.write(b'str(tn.host) + ":"+ str(tn.port)')
    mm = mmap.mmap(f.fileno(), 0)
    while True:
        try:
            msg = tn.read_eager()
            mm.resize(mm.size() + len(str(msg)))
            pdb.set_trace()
            print(type(msg))
            if msg != b'':
                # mm.write(msg)
                mm.flush()
            else:
                print("message is empty")
                pass
        except KeyboardInterrupt:
            print(" ,手动中断 ")
            break
            tn.close()
            mm.close()
            f.close()  # 双保险
            break
        except Exception as e:
            print(Exception , " : " , e)
            print(":(")
            print("你的电脑遇到问题，需要重新启动。你可以重新启动")
            tn.close()
            mm.close()
            f.close()   #双保险
            break

