#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo shows coroutine to operate async io with asyncio module
an event loop model to run multi tasks,
coroutine work with 'yield from'.
'''

import asyncio
import threading

# 装饰器标记generator为coroutine类型，可扔EventLoop去并发执行
@asyncio.coroutine
def assume_io():
    print('[%s]-->: Hello World!' % threading.current_thread())

    # 通过yield from可调用另一个generator/coroutine，并可获取返回值
    # yield from的coroutine执行时间比较长时，线程不等待事件立即返回，而中断并先执行消息循环下一个事件
    yield from asyncio.sleep(1)

    # 下次消息循环到达时，此前中断等待的事件若已返回，则继续往下执行
    print('[%s]-->: I am cent.' % threading.current_thread())


@asyncio.coroutine
def get_web(host):
    print('get web: %s' % host)

    # 异步连接http服务
    reader, writer = yield from asyncio.open_connection(host, 80)

    # 继续执行，并异步发送http GET web请求
    header = 'GET / HTTP/1.0\r\nHost:%s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    # drain刷新写入缓冲区，yield from coroutine，不用等待时，会立即继续执行
    yield from writer.drain()

    while True:
        # 异步读取数据
        line = yield from reader.readline()

        if line == b'\r\n':
            break

        print('%s header --> %s' % (host, line.decode('utf-8').rstrip()))

    # 结束则关闭请求写入传输
    writer.close()

def test_asyncio():
    # test multi-async-tasks running

    # 获取multi tasks轮询EventLoop
    loop = asyncio.get_event_loop()

    print('test multi-async-tasks')
    tasks = [assume_io(), assume_io()]
    # 多个任务扔进EventLoop轮询执行
    #loop.run_until_complete(asyncio.wait(tasks))

    print('test get web using async-io')
    new_tasks = [get_web(host) for host in ['www.baidu.com', 'www.sina.com.cn', 'www.163.com']]
    tasks.extend(new_tasks)
    # 多个任务扔进EventLoop轮询执行
    loop.run_until_complete(asyncio.wait(tasks))

    #结束则关闭EventLoop消息循环
    loop.close()

# todo some test
if __name__ == '__main__':
    test_asyncio()