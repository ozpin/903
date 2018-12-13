#!/usr/bin/python3
#Author:sean

import selectors
import socket
#selectors模块默认会用epoll，如果你的系统中没有epoll(比如windows)则会自动使用select
sel = selectors.DefaultSelector()   #生成一个select对象

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False) #设定非阻塞
    sel.register(conn, selectors.EVENT_READ, read)  #新连接注册read回调函数

def read(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 8080))
sock.listen()
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)    #把刚生成的sock连接对象注册到select连接列表中，并交给accept函数处理

while True:
    events = sel.select()   #默认是阻塞，有活动连接就返回活动的连接列表
    print(events)

    #这里看起来是select，其实有可能会使用epoll，如果你的系统支持epoll，那么默认就是epoll
    for key, mask in events:
        print("key",key)
        print("mask",mask)
        callback = key.data     #去调accept函数
        callback(key.fileobj, mask) #key.fileobj就是readable中的一个socket连接对象