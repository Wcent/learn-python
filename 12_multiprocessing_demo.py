#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about multiprocessing
多进程示例，介绍Process创建进程对象启动单个进程、Pool进程池批量创建，
及进程间通信Queue/Pipe交换数据（生产者-消费者模式）
'''

import os
from multiprocessing import Process, Queue
from multiprocessing import Pool
import time, random

# fork() only works on Unix/Linux/Mac but not works windows
def test_fork():
    print('Test fork: ')
    print('Process (%s) is start...' % os.getpid())

    # only works on Unix/Linux/Mac:
    pid = os.fork()
    if pid == 0:
        print('I am a child process (%s) and my parent process is (%s)' % (os.getpid(), os.getppid()))
    else:
        print('I (%s) just create a child process (%s)' % (os.getpid(), pid))

# 创建子进程时传入的目标处理函数
def call_proc(args):
    print('%s: running a child process (%s)' % (args,os.getpid()))

# Process创建子进程
def test_process():
    print('Test Process: ')
    print('Parent process (%s).' % os.getpid())

    # new a child process
    p = Process(target=call_proc, args=('test',))
    print('A child process will start.')

    # 启动子进程
    p.start()
    # 等待子进程结束，再继续执行（可用于进程间的同步）
    p.join()

    print('The child process end.')


# 目标函数
def long_time_task(args):
    print('%s: Run task (%s).' % (args,os.getpid()))
    start = time.time()

    # wait a moment
    time.sleep(random.random()*3)
    end = time.time()
    print('Task %s run %0.2f seconds.' % (os.getpid(), end-start))

# Pool进程池批量创建子进程
def test_pool():
    print('Test Pool: ')
    print('Parent process (%s).' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocessing done...')

    # close后不允许再创建添加新的子进程
    p.close()

    # 等待所有子进程结束，调用前要先close
    p.join()

    print('All subprocess done.')

# 生产者：将数据写进Queue以传递
def write_prc(q):
    print('Process (%s) to write' % os.getpid())
    for value in ['A', 'B', 'C', 'D']:
        print('Producer: Put (%s) to queue.' % value)
        q.put(value)
        time.sleep(random.random())

# 消费者：从Queue获取数据以处理
def read_prc(q):
    print('Process (%s) to read' % os.getpid())
    while True:
        value = q.get(True)
        print('Consumer: Get (%s) from queue.' % value)

# 创建2个进程，使用Queue实现进程间通信，模拟生产者-消费者模式
def test_producer_consumer():
    print('Test Queue:')
    q = Queue()
    # 进程使用Queue对象通信
    pw = Process(target=write_prc, args=(q,))
    pr = Process(target=read_prc, args=(q,))

    # 启动进程写/读
    pw.start()
    pr.start()

    # 等待写进程结束
    pw.join()
    # 读进程为死循环，只能父进程强行终止
    pr.terminate()

if __name__ == '__main__':
    #test_fork()

    test_process()

    test_pool()

    test_producer_consumer()