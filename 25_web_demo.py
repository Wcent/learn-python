#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo develop web app with flask a web framework

'''

from flask import Flask
from flask import request

web_app = Flask(__name__)

@web_app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@web_app.route('/signin', methods=['GET'])
def signin_form():
    html = '''
    <form action="/signin" method="post">
    <p>username: <input name="username"></p>
    <p>password: <input name="password" type="password"></p>
    <p><button type="submit">Sign In</button></p>
    </form>
    '''
    return html

@web_app.route('/signin', methods=['POST'])
def signin():
    # 可从request对象中读取表单内容
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h1>Hello, World!</h1>'
    return '<h3>wrong username or password.</h3>'

# todo some test
if __name__ == '__main__':
    web_app.run()