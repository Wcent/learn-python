#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo shows using flask and template to develop web app with MVC 
web app same as 25_web_demo but implement with template
'''

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('signin_form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        return render_template('signin_ok.html', username=username)
    return render_template('signin_form.html', message='wrong username or password', username=username)

# todo some test
if __name__ == '__main__':
    app.run()