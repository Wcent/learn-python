#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about how to use enumeration
'''

from enum import Enum, unique

# define a custom enumeration by inheriting from base class Enum
# the decorator with key word @unique make sure to include no duplication member
# 继承方式定制枚举类型,@unique装饰器保证元素唯一性
@unique
class Week(Enum):
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6

# define an enum object directly
# 直接定义枚举类型实例
month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'))

# testing
if __name__ == '__main__':
    print(Week.Saturday)
    print(month.Jan)
    print(month['Mar'])
    print(month(12))

    for day in Week.__members__.items():
        print(day)

    for name,member in month.__members__.items():
        print(name, '==>', member.value)