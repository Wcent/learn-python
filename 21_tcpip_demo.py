#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about tcp/ip network shows how to program with socket.
TCP：通信双方建立可靠连接，以流形式发送接收数据
UDP：面向无连接
'''

import socket
import threading

# test tcp in client
def tcp_in_client():
    # 创建一个socket，AF_INET: IPv4 (AF_INET6: IPv6), SOCK_STREAM：面向流TCP协议
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 建立连接，参数为tuple，包含地址和端口
    s.connect(('www.sina.com.cn', 80))

    # 发送数据，这里为HTTP GET请求，请求新浪主页
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnect: close\r\n\r\n')

    buffer = []
    while True:
        # 接收响应数据，指定每次最多接收数据量
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break

    # 连接接收到的数据
    data = b''.join(buffer)

    # 关闭连接
    s.close()

    # 分离HTTP头和html
    header, html = data.split(b'\r\n\r\n', 1)
    print(header.decode('utf-8'))
    # 接收到的html数据写入文件保存
    #with open('test.html', 'wb') as f:
    #    f.write(html)


# process tcp link from client in server
def tcp_link_prc(sock, addr):
    print('Accept new connection from (%s:%s)' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        if not data or data.decode('utf-8') == 'quit':
            break
        sock.send(('Hello, %s' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from (%s:%s) closed.' % addr)

# test tcp in server
def tcp_in_server():
    # 创建socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定端口
    s.bind(('127.0.0.1', 9999))

    # 监听绑定的端口
    s.listen(5)
    print('Waiting for connection...')

    # server一般通过永久循环，不断等待接受连接
    while True:
        # 等待接受来自客户端新连接
        sock, addr = s.accept()

        # 创建新线程处理TCP连接
        t = threading.Thread(target=tcp_link_prc, args=(sock, addr))
        t.start()

# testing client link to server
def test_client_link():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9999))
    print(s.recv(1024).decode('utf-8'))

    for data in [b'cent', b'lina', b'Python', b'world']:
        s.send(data)
        print(s.recv(1024).decode('utf-8'))
    s.send('quit')
    s.close()


# test udp in server
def udp_in_server():
    # SOCK_DGRAM：UDP类型socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定端口，服务端UDP socket不需要监听端口，直接接收来自客户端的数据
    s.bind(('127.0.0.1', 8888))
    print('Bind UDP on 8888...')

    while True:
        # 接收客户端数据、地址及端口
        data, addr = s.recvfrom(1024)
        print('Received from (%s:%s)' % addr)

        # 通过UDP协议给客户端发送数据
        s.sendto(b'UDP server prc: %s' % data, addr)

# test udp in client
def udp_in_client():
    # 客户端UDP socket，不需要连接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for data in [b'python', b'hello, world']:
        # 直接发送数据
        s.sendto(data, ('127.0.0.1', 8888))
        # 接收数据
        print(s.recv(1024).decode('utf-8'))
    s.close()


# todo some test
if __name__ == '__main__':
    #tcp_in_client()

    #tcp_in_server()

    udp_in_server()