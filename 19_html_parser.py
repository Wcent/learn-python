#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about html parser.
parser.feed()接受str，html太大允许多次feed解析
'''

from html.parser import HTMLParser
from urllib.request import urlopen


# 通过html pareser对象feed解析，触发相应事件处理
class TestHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print('Start tag: %s, attrs: %s' % (tag, attrs))

    def handle_endtag(self, tag):
        print('End tag: %s' % tag)

    def handle_data(self, data):
        print('Data: %s' % data)

    def handle_comment(self, data):
        print('Comment: %s' % data)

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, decl):
        print('Decl: %s' % decl)


# test html parser
if __name__ == '__main__':
    with urlopen('https://www.baidu.com') as f:
        html = f.read()
        html_parser = TestHtmlParser()
        html_parser.feed(html.decode('utf-8'))