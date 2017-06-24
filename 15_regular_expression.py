#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about regular expression and re module
\d: 数字
\w: 字母或数字
\s：空格（包含tab等空白符）
. : 任意字符
* ：任意个（包含0）
+ ：至少一个
? ：0个或1个，默认正则表达式贪婪匹配，即匹配尽可能多的字符，而使用'?'则是匹配尽可能少字符
- ：表示范围，使用'-'特殊字符时需要转义
\ ：特殊字符，使用'\'需要转义
| ：或
[]：表示范围
()：分组
{n}：n个
{n,m}：n到m个
^ ：表示行开头
$ ：表示行结束
'''

import re

# 测试re模块正则表达式匹配使用
def re_match(pattern, string):
    print('Test regular expression:')
    if re.match(pattern, string):
        print('%s is OK!' % string)
    else:
        print('Not match: %s' % string)

# testing
if __name__ == '__main__':

    # 正则表达式含义：匹配合法的变量命名，表达式前缀r，表明\本身不需要考虑转义
    re_var_name = r'[a-zA-Z\_][0-9a-zA-Z\_]*'
    re_match(re_var_name, '_var_name')
    re_match(re_var_name, 'var_name')
    re_match(re_var_name, '9_cent')

    # 正则表达式含义：匹配电话号码，3到4位区号开头，3到8位号码结尾，中间任意空格加-分隔
    re_tel_number = r'^(\d{3,4})\s*\-\s*(\d{3,8})$'
    re_match(re_tel_number, '020-88888123')
    re_match(re_tel_number, '0755 - 86206198')
    re_match(re_tel_number, ' - 59101234')
    re_match(re_tel_number, '123a - 123456')
    re_match(re_tel_number, '12345678')
    re_match(re_tel_number, '0755 - 123456789')

    # 正则表达式的使用re模块会先编译表达式，后匹配，频繁使用正则表达式，降低效率，可预编译好规则，直接使用匹配，优化性能
    print('Test re complie: ')
    # 编译生成regular expression对象，包含正则表达式，后续直接调用方法匹配字符串
    re_tel_number_complie = re.compile(re_tel_number)
    print(re_tel_number_complie.match('0755 - 12345678').groups())

    #测试re模块使用正则表达式分割字符串
    print('Test regular split string: ')
    text = '2017/6/20 21:05	Platform and Plugin Updates: PyCharm Community Edition is ready to update.'
    str_group = re.split(r'[\s*\,\;\.\:\!\?]+', text)
    for str in str_group:
        print(str)
