#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
A demo about xml parser. 
It shows a SAX xml parser how to work.
DOM：解析xml时，整个xml读入内存，生成解析树
SAX：使用流模式解析，即边读边解析
示例测试SAX解析器机制
sax.parseString()传入解析xml及处理解析事件ContentHandler对象
sax.parse()类似针对xml文件解析
'''

from xml import sax
import re

# 解析xml触发ContentHandler相应事件处理
class SaxContentHandler(sax.ContentHandler):
    # 解析到xml节点
    def startDocument(self):
        print('sax: startDocument')

    # 解析到tag
    def startElement(self, name, attrs):
        print('sax: startElement: %s' % name)
        if 'type' in attrs:
            print('attrs: %s' % attrs['type'])
        if 'href' in attrs:
            print('attrs: %s' % attrs['href'])

    # 解析xml内容
    def characters(self, content):
        if re.match(r'\s+|\n+', content) is None:
            print('sax: characters: %s' % content)

    # 解析tag结束
    def endElement(self, name):
        print('sax: endElement: %s' % name)

    # 解析节点结束
    def endDocument(self):
        print('sax: endDocument')


# test xml sax parser
if __name__ == '__main__':
    xml = r'''<?xml version="1.0"?>
    <topic type="python">
    <title href="/python">Python</title>
    <content href="/hello_world">Hello World!</content>
    </topic>
    '''
    sax.parseString(xml, SaxContentHandler())