'''
聊天室服务端
'''
import os
from socket import *

ADDR = ('127.0.0.1',8000)

user = {}

#敏感词汇
sensitivity = ['操','日']

# 用户违规次数
squint_count = {}

#登陆处理
def enter(sockfd,name,addr):
    if name in user or '管理员' in name:
        sockfd.sendto('该用户已存在'.encode(), addr)
    sockfd.sendto(b'OK', addr)
    for i in user:
        if i != name:
            info = '\n%s: 进入了聊天室'%name
            sockfd.sendto(info.encode(),user[i])
        else:
            info = '\n您已进入了聊天室'
            sockfd.sendto(info.encode(),addr)
    user[name] = addr

#聊天
def chat(sockfd,name,msg):
    for i in user:
        if i != name:
            info = '\n%s: %s'%(name,msg)
            sockfd.sendto(info.encode(),user[i])

    check(msg, name, sockfd)

#敏感词汇检测
def check(msg, name, sockfd):
    for item in sensitivity:
        if item in msg:
            if name in squint_count:
                warn_dispose(name, sockfd)
            else:
                squint_count[name] = 1
                info = '\n管理员: %s请文明发言,警告%d次,最高三次' % (name, 1)
                for i in user:
                    sockfd.sendto(info.encode(), user[i])

#警告处理
def warn_dispose(name, sockfd):
    squint_count[name] += 1
    if squint_count[name] == 3:
        sockfd.sendto('quit'.encode(), user[name])
        del user[name]
        for i in user:
            info = '\n%s 已被踢出聊天室' % name
            sockfd.sendto(info.encode(), user[i])
    else:
        info = '\n管理员: %s请文明发言,警告%d次,最高三次' % (name, squint_count[name])
        for i in user:
            sockfd.sendto(info.encode(), user[i])

#退出聊天室
def quit(sockfd,name):
    for i in user:
        if i != name:
            info = '%s: 退出了聊天室'%name
            sockfd.sendto(info.encode(),user[i])
        sockfd.sendto(b'quit',user[name])
    del user[name]

#处理用户请求
def do_request(sockfd):
    while True:
        msg,addr = sockfd.recvfrom(1024)
        data = msg.decode().split(' ',2)
        if data[0] == 'E':
            enter(sockfd,data[1],addr)
        elif data[0] == 'C':
            chat(sockfd,data[1],data[2])
        elif data[0] == 'Q':
            quit(sockfd,data[1])

# 管理员消息
def admin_msg(sockfd):
    while True:
        msg = input('管理员:')
        info = 'C 管理员 %s'%msg
        # 注意此时user中为空字典,因为开启了两个进程,字典添加操作在另一个进程，
        # 这个进程无法使用,所以采用sockfd.sendto(info.encode(),ADDR)方式来解决
        sockfd.sendto(info.encode(),ADDR)

# 服务端启动
def main():
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)
    pid = os.fork()
    if pid == 0:
        do_request(sockfd)
    else:
        admin_msg(sockfd)                 #管理员消息

main()



