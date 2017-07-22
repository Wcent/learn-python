#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
A demo about database.
Using SQLite & MySQL to do some test.
'''

import sqlite3
import mysql.connector
from contextlib import closing

#===========================================================================
# demo about sqlite3
#===========================================================================
def test_sqlite():
    print('Test sqlite:')
    sqlite_create_table()
    sqlite_insert()
    sqlite_select()
    sqlite_delete()

# create table demo
def sqlite_create_table():
    try:
        # 连接数据库，test.db文件不存在，则在当前目录下新建
        db_connect = sqlite3.connect('test.db')

        # 创建cursor对象，用于操纵执行SQL语句
        cursor = db_connect.cursor()

        # 构造新建表sql语句，表不存在则新建
        sql = '''create table if not exists stocks
        (date text, trans text, symbol text, quantity real, price real)'''
        cursor.execute(sql)

    except sqlite3.Error as e:
        print('SQLite3 Error occurred: %s' % e)

    finally:
        # 使用完确保cursor需要关闭释放
        cursor.close()

        # 手动提交事务，con.close()不会自动处理事务
        db_connect.commit()

        # 使用完确保connect需要关闭释放
        db_connect.close()

# insert record demo
def sqlite_insert():
    #使用context manager管理数据库连接，自动处理事务，异常回滚，否则提交事务
    with sqlite3.connect('test.db') as db_connect:
        cursor = db_connect.cursor()

        # 使用参数（?为占位符）构造sql语句代替直接字符串，可避免SQL注入攻击
        cursor.execute('select * from stocks where symbol = ?', ('RHAT',))

        #记录不存在则插入
        if not cursor.fetchall():
            sql = '''insert into stocks(date, trans, symbol, quantity, price)
            values(?, ?, ?, ?, ?)'''
            cursor.execute(sql, ('2017-07-15', 'BUY', 'RHAT', 100, 35.14))

            # with...as...context manager内亦可手动提交事务
            db_connect.commit()
            print('Insert %s records.' % cursor.rowcount)

        # 一次插入多条记录
        purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                     ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                     ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                     ]
        cursor.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

        # 关闭释放cursor
        cursor.close()

        # 影响记录数目反映到rowcount
        print('Insert %s records.' % cursor.rowcount)

# delete all record demo
def sqlite_delete():
    with sqlite3.connect('test.db') as db_connect:
        cursor = db_connect.cursor()
        cursor.execute('delete from stocks')
        print('Delete %s reords.' % cursor.rowcount)
        cursor.close()

def sqlite_select():
    with sqlite3.connect('test.db') as db_connect:
        cursor = db_connect.cursor()

        # retrieve data style 1: call method fetchone() or fetchall()
        cursor.execute('select * from stocks where symbol = ?', ('IBM',))
        print('select & fetchone:', cursor.fetchone())

        # retrieve data style 2: treat the cursor as an iterator
        for row in cursor.execute('select * from stocks order by price'):
            print(row)

        cursor.close()
#===========================================================================
# sqlite3 demo end
#===========================================================================


#===========================================================================
# demo about mysql
#===========================================================================
def test_mysql():
    print('Test mysql:')
    mysql_create_table()
    mysql_insert()
    mysql_select()
    mysql_delete()

def mysql_create_table():
    try:
        db_connect = mysql.connector.connect(user='root', password='******', database='test')
        cursor = db_connect.cursor()
        cursor.execute('create table if not exists users(id varchar(20) primary key, name varchar(20))')
        db_connect.commit()

    except mysql.connector.Error as e:
        db_connect.rollback()
        print('Error occurred: %s' % e)

    finally:
        cursor.close()
        db_connect.close()

def mysql_insert():
    # contextlib.closing()使得mysql connect可用于with...as...context manager
    with closing(mysql.connector.connect(user='root', password='******', database='test')) as db_connect:
        cursor = db_connect.cursor()

        # mysql使用%s作为参数占位符构造sql语句
        cursor.execute('select * from users where id = %s', ('1',))
        if not cursor.fetchall():
            cursor.execute('insert into users(id, name) values(%s, %s)', ('1', 'cent'))
            db_connect.commit()
            print('Insert %s records successfully!' % cursor.rowcount)
        cursor.close()

def mysql_delete():
    with closing(mysql.connector.connect(user='root', password='686905', database='test')) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute('delete from users')
        db_connect.commit()
        print('%s records deleted.' % cursor.rowcount)
        cursor.close()

def mysql_select():
    with closing(mysql.connector.connect(user='root', password='686905', database='test')) as db_connect:
        cursor = db_connect.cursor()
        cursor.execute('select * from users')
        print(cursor.fetchall())
        cursor.close()
#===========================================================================
# mysql demo end
#===========================================================================


# do some test
if __name__ == '__main__':
    test_sqlite()
    test_mysql()