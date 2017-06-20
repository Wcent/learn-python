#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
A demo shows how multi-process works in distributed system using queue with manager module.
Here is a sample master-worker model.
The master send tasks to queue registered on network by class inherit from BaseManager in manager module
to provide interface, while workers access tasks from queue registered.

manager模块支持进程分布式，
示例实现简单的master/worker模型，一个服务进程作为调度者，分派任务，多个客户进程作为执行者，接受任务并执行，
master/worker之间通过网络关联通讯访问，继承manager模块BaseManager的类对象管理queue，将queue注册到网络，暴露访问接口。
注意queue的作用是传递任务和接受结果，适合发送任务描述等小数据量，如发送数据的具体访问路径，处理进程再到具体路径去数据处理。
'''

import random, queue
from multiprocessing.managers import BaseManager


# inherit from BaseManager
class QueueManager(BaseManager):
    pass

# 定义任务/结果队列
task_queue = queue.Queue()
result_queue = queue.Queue()

def get_task_queue():
    global task_queue
    return task_queue

def get_result_queue():
    global result_queue
    return result_queue


# master: sending tasks & receiving result
def master():
    # 定义任务/结果队列
    #task_queue = queue.Queue()   # doesn't work on windows
    #result_queue = queue.Queue() # doesn't work on windows

    #QueueManager.register('get_task_queue', callable=lambda : task_queue) # doesn't work on windows
    #QueueManager.register('get_result_queue', callable=lambda : result_queue) # doesn't work on windows

    # 队列注册到网络可访问接口（自定义访问接口），callable参数关联Queue对象
    # Manager服务进程持有Queue对象，客户进程可链接服务进程获取Manager代理对象，从而访问Queue对象
    QueueManager.register('get_task_queue', callable=get_task_queue)
    QueueManager.register('get_result_queue', callable=get_result_queue)

    # 绑定通讯ip地址及端口，设置验证码'cent'以保证链接可靠
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'cent')
    # 启动manager进程
    manager.start()

    # 通过注册接口获取网络访问Queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 通过queue发送分派任务
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task: (%s)' % n)
        task.put(n)

    # 从queue接受返回结果
    for i in range(10):
        r = result.get(timeout=10)
        print('Get result: (%s)' % r)

    # 关闭manager进程
    manager.shutdown()
    print('Master end.')


# worker code runs in other machines
#import queue
#from multiprocessing.managers import BaseManager

#class QueueManager(BaseManager):
#    pass

# worker: receiving tasks, processing & returning result
def worker():
    # worker注册网络接口，以获取服务进程定义的Queue对象
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    # 运行master进程的服务器
    server_adr = '127.0.0.1'
    print('Connect to server %s...' % server_adr)

    # 获取manager进程代理对象，地址、端口、验证码与master设置一致以连接访问
    manager = QueueManager(address=(server_adr, 5000), authkey=b'cent')
    # 通过网络连接
    manager.connect()

    # 获取Queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 从task队列接受任务，处理并将结果返回result队列
    for i in range(10):
        try:
            n = task.get(timeout=1)
            print('receive task(%s), processing')
            result.put(('str(%s)' % n))
        except queue.Queue.Empty:
            print('Task queue is empty.')
    print('Worker End.')


def test_distribute_process():
    master()

# testing
if __name__ == '__main__':
    test_distribute_process()