import select
import time
import socket
import random
import threading

address = ('127.0.0.1',31500)

epoll=select.epoll()

connects={}

def registerSocketToEpoll():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    s.sendto('a'*1,address)
#    s.setblocking(False)
#    s.settimeout(1)
    #epoll.register(s.fileno(),select.EPOLLIN|select.EPOLLET)
    threadLock.acquire()
    epoll.register(s.fileno(),select.EPOLLIN)
    connects[s.fileno()]={'sock':s,'timeout':random.uniform(10,30),'oldtime':time.time()}
    threadLock.release()

def newRatePerSec(num):
    for x in range(num):
        registerSocketToEpoll()

def newRate(total,duration):
    quotient=total/duration
    remainder=total%duration
    for x in range(quotient):
        oldTime=time.time()
        if x == quotient-1:
            newRatePerSec(remainder+duration)
        else:
            newRatePerSec(duration)
        sleepTime=1-(oldTime-time.time())
        if sleepTime > 0 :
            time.sleep(sleepTime)

def get_socket(connects):
    return [ connects[x]['sock'].fileno() for x in connects.keys() ]
#    return map(lambda x:connects[x]['sock'].fileno(),connects.keys())

def distinguish_socket_by_epoll(all_sockets,epoll_sockets):
#    epoll_fileno=get_fd_from_epoll(epoll_sockets)
    epoll_fileno=[ x[0] for x  in epoll_sockets]
    return set(all_sockets)-set(epoll_fileno)

def get_fd_from_epoll(epoll_list):
    return [ x[0] for x in epoll_list ]
#    return map(lambda x:x[0],epoll_list)

threadLock=threading.Lock()
t=threading.Thread(target=newRate,args=(10000,300))
t.start()

while True:
    #threadLock.acquire()
    epoll_list=epoll.poll(timeout=1)
    have_sock=get_socket(connects)
    #threadLock.release()
    unactive_sockets=distinguish_socket_by_epoll(have_sock,epoll_list)
    for fd,event in epoll_list:
        if event & select.EPOLLERR :
            print("have error fileno :{} ".format(fd))
            connects[fd].sendto('b'*100,address)
        elif event & select.EPOLLIN:
            now=time.time()
            if now-connects[fd]['oldtime'] > connects[fd]['timeout']:
                print("fd :{} ,timeout:{} ,c ".format(fd,connects[fd]['timeout']))
                connects[fd]['sock'].sendto('c'*10,address)
                connects[fd]['oldtime'] = now
        elif event & select.EPOLLOUT:
            print("have register event")
        else :
            print("test")

    for fd in unactive_sockets:
        now=time.time()
        if now-connects[fd]['oldtime'] > connects[fd]['timeout']:
            print("fd :{} ,timeout:{} ,time:{} ,d".format(fd,connects[fd]['timeout'],time.time()))
            connects[fd]['sock'].sendto('d'*15,address)
            connects[fd]['oldtime'] = now
        
