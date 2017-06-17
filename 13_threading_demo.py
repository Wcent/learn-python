#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo shows how to use multi-thread with threading module
使用threading模块执行多线程任务，
lock加锁保证线程共享数据修改确定性，ThreadLocal机制实现线程间数据传递，并且数据独立
'''

import threading, time


def misson_one_prc():
    print('thread (%s) is running.' % threading.current_thread().name)
    for i in range(3):
        print('thread (%s) does print %s' % (threading.current_thread().name, i))
        time.sleep(1)
    print('thread (%s) end.' % threading.current_thread().name)

def misson_two_prc():
    print('thread (%s) is running.' % threading.current_thread().name)
    for i in range(5):
        print('thread (%s) does print %s' % (threading.current_thread().name, i))
        time.sleep(1)
    print('thread (%s) end.' % threading.current_thread().name)


def test_thread():
    print('Test multi-thread: ')
    print('Thread (%s) is running' % threading.current_thread().name)
    t1 = threading.Thread(target=misson_one_prc, name='misson_one_prc')
    t2 = threading.Thread(target=misson_two_prc, name='misson_two_prc')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('Thread (%s) end.' % threading.current_thread().name)

# test lock for multi-thread
# 使用资源锁，保证共享数据修改确定性，try...finally确保锁使用完后释放
# （使用锁降低了cpu效率，只有获利锁的一个线程在跑，其他线程等待锁）

rst = 0 # 共享数据
lock = threading.Lock() # 资源锁

def change(n):
    global rst
    rst = rst + n
    rst = rst - n

# 没有加锁对共享数据修改，多个线程跑，数据出现不确定性
def unlock_change(n):
    for i in range(100000):
        change(n)

# 加锁修改共享数据，多个线路跑，保证获取到锁的线程才能修改数据
def lock_change(n):
    global lock
    for i in range(100000):
        # 获取锁
        lock.acquire()
        try:
            change(n)
        finally:
            # 最后释放锁
            lock.release()

# 两个线程对共享数据修改
def test_change(func):
    global rst
    rst = 0
    t1 = threading.Thread(target=func, args=(5,))
    t2 = threading.Thread(target=func, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('Thread (%s) Rst: %s' % (func.__name__, rst))

# 无锁、加锁2种方式使用多线程修改数据
def test_two_way():
    print('Test Lock:')
    test_change(unlock_change)
    test_change(lock_change)



# ThreadLocal实现线程间数据传递，数据独立互不影响，不需要加锁访问
resource = threading.local() # 创建全局thread local

def task_prc():
    # 获取当前线程关联obj
    obj = resource.task_obj
    print('thread (%s) is running, processing object (%s)' % (threading.current_thread().name, obj))

def thread_task(obj):
    # 线程关联绑定obj
    resource.task_obj = obj
    task_prc()

# 创建多个线程，不同线程传入不同对象处理，互相独立不影响
def test_thread_local():
    print('Test ThreadLocal: ')
    for i in range(5):
        t = threading.Thread(target=thread_task, args=('Obj_'+str(i),), name='Misson_'+str(i))
        t.start()


# testing
if __name__ == '__main__':
    #test_thread()

    test_two_way()

    test_thread_local()