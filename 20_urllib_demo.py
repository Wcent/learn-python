#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about urllib module, including some operation of url like GET/POST. 
'''

from urllib import request, parse

# GET request & response of http
def test_get(url):
    with request.urlopen(url) as f:
        data = f.read()
        print('Status: (%s, %s)' % (f.status, f.reason))
        for item in f.getheaders():
            print('%s: %s' % item)
        print('Data: %s' % data.decode('utf-8'))

# masquerade browser to send GET request
def get_like_browser(url):
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone: CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26'
                   '(KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    with request.urlopen(req) as f:
        print('Status: (%s, %s)' % (f.status, f.reason))
        for item in f.getheaders():
            print('%s: %s' % item)
        print('Data: %s' % f.read().decode('utf-8'))


# post like a browser, test to login weibo
def test_post():
    print('Test Post to Login weibo.cn:')
    user = input('username/email/phone_number:')
    password = input('password:')
    post_login_data = parse.urlencode([
        ('username', user),
        ('password', password),
        ('entry', 'mweibo'),
        ('client_id', ''),
        ('savestate', 1),
        ('ec', ''),
        ('pagrefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
    ])

    req = request.Request('https://passport.weibo.cn/sso/login')
    req.add_header('Origin', 'https://passport.weibo.cn')
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X)'
                   ' AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    req.add_header('Referer', 'https://passport.weibo.cn/signin/login'
                              '?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')

    # post like a browser, post_data must turns to be bytes
    with request.urlopen(req, data=post_login_data.encode('utf-8')) as f:
        print('Status: (%s, %s)' % (f.status, f.reason))
        for item in f.getheaders():
            print('%s: %s' % item)
        print('Data: %s' % f.read().decode('utf-8'))


# testing
if __name__ == '__main__':
    test_get(r'https://api.douban.com/v2/book/2129650')

    get_like_browser(r'http://www.douban.com/')

    test_post()