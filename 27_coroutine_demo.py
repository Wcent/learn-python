#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about coroutine, 
shows how to use yield and send to implement a producer-consumer model.
'''

# 生产者，接受生成器(generator)对象参数
def producer(c):
    for i in range(10):
        if i == 0:
            print('[Producer]->: Get consumer ready!')
            # 首先得启动generator，不能send non-None值
            result = c.send(None)
        else:
            print('[Producer]->: producing %s' % i)
            # 发送数据到generator，中止当前流程并切换转到generator执行，
            # 等generator处理yield返回数据，从send接受后再继续执行
            result = c.send(i)
        print('[Producer]->: consumer return %s' % result)

    print('[Producer]->: End producing!')
    # 最后关闭generator
    c.close()

# 消费者，定义为yield函数，可以返回generator对象，以支持协程(coroutine)
def consumer():
    result = 'Start'
    while True:
        # 通过yield接受数据，处理，最后再通过yield返回数据
        i = yield result

        # 接受不到数据，直接返回，注意外层需要捕获generator StopIteration异常
        if not i:
            return

        print('[Consumer]->: consuming %s' % i)
        result = 'Done'

# todo some test
if __name__ == '__main__':
    # 创建generator对象，通过coroutine实现生产者消费者模式
    c = consumer()
    producer(c)