#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about exception to handle error at runtime
'''

import logging

# 设置日志文件log.log
logging.basicConfig(filename='./log.log', level=logging.DEBUG)

# testing try...exception...else...finally with division
def divide(a, b):
    try:
        print('try...')
        result = a / int(b)
        print('result: ', result)
        return result
    except ValueError as e:
        print('ValueError: ', e)
    except ZeroDivisionError as e:
        print('ZeroDivisionError: ', e)

    # 异常为类，父类可以except捕获处理时，后面的子类不能再捕获，
    except BaseException as e:
        print('BaseException: ', e)
        logging.exception(e)

    # never run after BaseException
    except Exception as e:
        print('Exception: ', e)

    # 存在finally语句时，正常异常都会运行（注意，前面存在return时，依然运行finally，但End语句不会再跑）
    finally:
        print('finally...')
    print('End')

# testing
if __name__ == '__main__':
    divide(10, 'a')
    divide(10, '0')
    divide('10', 5)
    divide(10, '3')
    divide(10, 2)