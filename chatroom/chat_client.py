'''
聊天室客户端
'''
from socket import *
import os,sys

# 服务器地址
ADDR = ('127.0.0.1',8000)

# 发送消息
def send_msg(sockfd,name):
    while True:
        try:
            msg = input('头像:')
        except KeyboardInterrupt:
            print('谢谢使用')
            msg = 'quit'
        if msg.strip() == 'quit':
            info = 'Q ' + name
            sockfd.sendto(info.encode(),ADDR)
            sys.exit('您已退出聊天室')

        # 'C name 内容'
        else:
            info = 'C %s %s'%(name,msg)
            sockfd.sendto(info.encode(),ADDR)

# 接收消息
def recv_msg(sockfd):
    while True:
        msg,addr = sockfd.recvfrom(1024)
        if msg.decode() == 'quit':
            sys.exit()
        info = msg.decode() + '\n头像:'
        print(info,end='')

#登录函数
def enter(sockfd):
    while True:
        try:
            name = input('请输入昵称:')
            if not name:
                continue
        except KeyboardInterrupt:
            print('谢谢使用')
            sys.exit()
        msg = 'E ' + name
        sockfd.sendto(msg.encode(),ADDR)
        data,addr = sockfd.recvfrom(1024)
        if data.decode() == 'OK':
            return name
        print(data.decode())

# 客户端启动
def main():
        sockfd = socket(AF_INET,SOCK_DGRAM)
        name = enter(sockfd)
        pid = os.fork()
        if pid == 0:
            send_msg(sockfd,name)  #发送消息
        else:
            recv_msg(sockfd)  #接受消息

main()









