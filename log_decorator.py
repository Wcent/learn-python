#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a sample to define a decorator implement by higher-order function
log function calling information
'''

import functools

# define a log decorator with two type:
# @log or @log('text')
# no param or one position param
# implement by higher-order function
def log(text_or_func):
    # while text_or_func is string, for type: @log('text')
    if isinstance(text_or_func, str):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print('calling begin: %s' % text_or_func)
                rtn = func(*args, **kwargs)
                print('calling end!')
            return wrapper
        return decorator

    # while text_or_func is function name, for type: @log
    else:
        @functools.wraps(text_or_func)
        def wrapper(*args, **kwargs):
            print('calling begin:')
            rtn = text_or_func(*args, **kwargs)
            print('calling end!')
            return rtn

        return wrapper

@log
def say_hi():
    print('say Hi in function %s' % say_hi.__name__)

@log
def say_hello(name):
    print('say Hello %s in function %s' % (name, say_hello.__name__))

@log('execute log information')
def say_haha():
    print('hahahahaha... in function %s' % say_haha.__name__)



# testing
if __name__ == '__main__':
    say_hi()
    say_hello('lina')
    say_haha()