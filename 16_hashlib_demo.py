#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo shows how to use MD5 or SHA1 with hashlib module
note:
# pseudo-code
if str == strA + strB
    hash.update(str) == hash.update(strA) + hash.update(strB)
'''

import hashlib

class Account(object):
    user = set()

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.user.add(username)

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, name):
        self.__username = name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    def login(self, username, password):
        if username not in self.user:
            print("user name '%s' is not exist! Please input the right name." % username)
            return
        if self.password != password:
            print("Password wrong! Please try again.")
            return
        print('Login sucessfully! Welcome %s' % self.username)


# get md5 hash value of str with hashlib module
def get_md5(str):
    md5 = hashlib.md5()
    # note: the string is added with salt
    md5.update((str+'the-Salt').encode('utf-8'))
    return md5.hexdigest()

# get md5 hash value of str without added salt
def get_md5_wihout_salt(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()

# get sha1 hash value of str with hashlib module
def get_sha1(str):
    sha1 = hashlib.sha1()
    # note: the string is added with salt
    sha1.update((str+'the-Salt').encode('utf-8'))
    return sha1.hexdigest()

# get sha1 hash value of str without added salt
def get_sha1_wihout_salt(str):
    sha1 = hashlib.sha1()
    sha1.update(str.encode('utf-8'))
    return sha1.hexdigest()


# testing
if __name__ == '__main__':
    print('Test MD5 and SHA1:')

    # init an acc with username and set password with the md5 hash value of password
    acc = Account('cent', get_md5('123456'))

    # test login
    acc.login('cent', get_md5('123456 '))

    # password set with md5 but try to login with sha1
    acc.login('cent', get_sha1('123456'))

    # try md5 hash value of password without salt
    acc.login('cent', get_md5_wihout_salt('123456'))

    # login with md5 hash value of the right password
    acc.login('cent', get_md5('123456'))

    # change password with the SHA1 hash value of password
    acc.password = get_sha1('password')

    # test login
    acc.login('cent', get_sha1('hello'))

    # try to login with the old md5 password
    acc.login('cent', get_md5('123456'))

    # try wrong user name
    acc.login('lina', get_sha1('password'))

    # login with sha1 hash value of the new password
    acc.login('cent', get_sha1('password'))