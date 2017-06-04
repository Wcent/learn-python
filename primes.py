#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a sample to use filter,
get primes by the Sieve of Eratosthenes
使用filter函数的简单例子，埃氏筛法求素数
'''

# define a prime iterator, retieve primes until the number guard or endless while guard is None
# 定义生成素数的迭代器，guard非None时获取小于guard的素数或者无限获取但guard为None
def primes(guard=None):
    if guard != None and guard < 2:
        return None

    # the first prime is 2
    yield 2

    # init an odd iterator start from 3
    it = __odd_iter()
    while True:
        # get the first one from the odd iterator
        n = next(it)

        # control getting primes less than guard
        if guard != None and guard < n:
            break

        yield n

        # filter the last iterator divided by n, therefore number in the last iterator not divided by n stay
        # and cover 'it' with a new filtered iterator (recursively filter)
        it = filter(__not_divisible(n), it)


# construct an odd iterator start from 3
# 构造从3开始的奇数迭代器，初始操作序列
def __odd_iter():
    n = 1
    while True:
        n += 2
        yield n

# construct a function not divisible by number
#构造非整除number函数，用于筛选序列
def __not_divisible(number):
    return lambda x: x % number > 0


# testing
if __name__ == '__main__':
    print('primes less than 10:')
    for prime in primes(10):
        print(prime)

    print('primes less than 100:')
    for prime in primes(100):
        print(prime)

    print('primes less than 10 by the other way:')
    primes_iter = primes()
    for p in primes_iter:
        if p < 10:
            print(p)
        else:
            break