#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about contextlib module, shows how to manage context.
'try ... finally' is the same as 'with ... as ...'
Defining a class which override '__enter__()' and '__exit__()' functions can be
used in 'with...as...' to implement context manager.
At the same time, decorator @contextmanager also can implement context manager simply,
 while decorator @closing just turn an object into context manager object.
'''

from contextlib import contextmanager
from contextlib import closing
from urllib.request import urlopen

# testing file operation
# while opening a file, it must be closed at last no matter error or not
def test_file_opr():
    # 'try ... finally...' implement context manager
    try:
        f = open('readme.md', 'r', encoding='utf-8')
        while True:
            line = f.readline()
            if not line:
                return
            print(line)
    finally:
        if f:
            f.close()

# the same as 'try ... finally...' but more simple
def test_same_file_opr():
    with open('readme.md', 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
               return
            print(line)


# override __enter__ and __exit__ function to implement with ... as... context manager
class Query(object):
    def __enter__(self):
        print('Begin to query:')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print('Error!')
        else:
            print('End query!')

    def query(self):
        print('to do query...')

# implement context manager with decorator '@contextmanager' in contextlib module
# the same as '__enter__()' and '__exit__()'
class SimpleQuery(object):
    def query(self):
        print('to do query...')

@contextmanager
def manager_query():
    print('Begin to query:')
    yield SimpleQuery()
    print('End query!')


# test @conextmanager and yield
@contextmanager
def tag(name):
    print('<%s>' % name)
    yield
    print('</%s>' % name)


# test decorator @closing to make an object to be a context manager object
# so that it can be used in with...as...
def test_closing_decorator():
    with closing(urlopen('https://www.python.org')) as page:
    #with closing(urlopen('https://www.baidu.com')) as page:
    #with urlopen('https://www.baidu.com') as page: # but it looks like this can work too. I don't know why yet.
        for line in page:
            print(line)


# testing
if __name__ == '__main__':
    print('Test context manager:')
    # test: try...finally
    test_file_opr()
    # test: with...as...
    test_same_file_opr()

    # test: @contextmanager
    with Query() as q:
        q.query()

    # with...as...语句先执行yield语句前代码，yield返回执行with语句内代码，最后执行yield语句后代码
    with manager_query() as sq:
        sq.query()

    with tag('html'):
        print('Hello World!')

    # test: @closing
    test_closing_decorator()