#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about operation of io(input/output),
shows how to read or write files
'''

# try...finally...确保open的file不管是否异常都会close释放资源
def io_one_way():
    try:
        f = open('readme.md', 'r', encoding='utf-8')

        # f.read()一次读完file里面的数据，如果内存不足，会抛出异常
        # content = f.read()

        # 更安全做法，f.read(size)，指定size字节，一次最多读入size字节的数据，多次调用直至file数据已读完
        while True:
            content = f.read(1024)

            # 读不到数据，数据为空时，结束
            if not content:
                print('read file EOF yet!')
                break
            print(content)

        f2 = open('1_hello_world.py', 'r')
        for line in f2.readlines():
            print(line)

    # open打开文件操作，使用完毕必须close关闭以释放，文件io可能会异常，确保close可以使用try...finally
    finally:
        if f :
            f.close()
            f2.close()

# with...as...确保open的file不管是否异常都会close释放资源，简化
def io_another_way():
    # with方式打开file操作，可以确保file最终被close释放掉（with语句会自动close隐式释放）
    with open('readme.md', 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()

            if not line:
                print('read file EOF yet!')
                break

            print(line)

    # file io read/write
    with open('10_io_demo.log', 'w+', encoding='utf-8') as f:
        f.write('测试io操作，read/write file!\n')
        f.write('Hello World!\n')

        # 重置文件指针，移至文件头
        f.seek(0)
        print(f.read())

# testing
if __name__ == '__main__':
    io_one_way()
    io_another_way()