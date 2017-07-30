#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about WSGI framework to develop web app
WSGI: Web Server Gateway interface
'''

from wsgiref.simple_server import make_server

# test first web app with wsgi
# WSGI接口定义要求的HTTP请求响应函数，接收2个参数
# environ：包含http所有请求信息的dict对象
# start_response：发送http响应header的函数
# 最后返回body
def hello_web(environ, start_response):
    # 响应返回http header，只能发送一次，即只需调用一次
    #响应头函数接收2个参数，响应码和list（包含http HEADER，2个str组成的tuple）
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 最后返回list对象包含http body，即html文档
    return [b'<h1>hello web</h1>']

# web app
def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 可分解env得到http请求信息，作相应处理，如可获得请求的url
    body = '<h1>Hello, %s!</h1>' % (env['PATH_INFO'][1:] or 'Web')
    return [body.encode('utf-8')]

def web_serve():
    # test hello web app
    #http_server = make_server('localhost', 8000, hello_web)

    # WSGI初始化服务，指定服务器ip，通过8000端口监听http请求，并注册响应函数application
    http_server = make_server('localhost', 8000, application)

    print('HTTP serve on port 8000...')

    # 启动http服务
    http_server.serve_forever()

# todo some test
if __name__ == '__main__':
    web_serve()