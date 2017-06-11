#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'


'''
a demo about pickle, shows how to serialize objects.
a extension sample of json which is common and standard. 
'''

import pickle
import json
from io import BytesIO
from io import StringIO

# shows pickle module to serialize and deserialize objects
# pickle: object <--> bytes
def test_pickle(dict_obj):
    print(dict_obj)

    # pickle.dumps()把任意对象序列化为bytes
    bytes = pickle.dumps(dict_obj)
    print(bytes)

    # pickle.loads()可以将bytes反序列化出对象
    obj_after = pickle.loads(bytes)
    print(obj_after)

    # change to test pickle.dump()/pickle.load()
    dict_obj['name'] = 'lina'
    dict_obj['sex'] = 'F'
    dict_obj['age'] = 18
    print(dict_obj)

    # pickle.dump()直接把对象序列化后写入file-like-object
    bytes_io = BytesIO()
    pickle.dump(dict_obj, file=bytes_io)

    # 重置指针指向类文件头
    bytes_io.seek(0)

    # pickle.load()直接从file-like-object中反序列化出对象
    obj_after = pickle.load(bytes_io)
    print(obj_after)

# shows json module to serialize and deserialize objects
# json: object <--> str
def test_json(dict_obj):
    print(dict_obj)

    # json.dumps()把任意对象序列化为bytes
    str = json.dumps(dict_obj)
    print(str)

    # json.loads()可以将bytes反序列化出对象
    obj_after = json.loads(str)
    print(obj_after)

    # change to test json.dump()/json.load()
    dict_obj['name'] = 'lina'
    dict_obj['sex'] = 'F'
    dict_obj['age'] = 18
    print(dict_obj)

    # json.dump()直接把对象序列化后写入file-like-object
    str_io = StringIO()
    json.dump(dict_obj, fp=str_io)

    # 重置指针指向类文件头
    str_io.seek(0)

    # json.load()直接从file-like-object中反序列化出对象
    obj_after = json.load(fp=str_io)
    print(obj_after)


# class to test json serialize and deserialize object
class People(object):
    def __init__(self, id, name, age, sex):
        self._id = id
        self._name = name
        self._age = age
        self._sex = sex

    def __str__(self):
        print('People: (id:%s, name:%s, age:%s, sex:%s)' % (self._id, self._name, self._age, self._sex))

# to make object of People serializable: object --> dict
def people2dict(p):
    return {'id':p._id, 'name':p._name, 'age':p._age, 'sex':p._sex}

# to make object of People deserializable: dict --> object
def dict2people(dict):
    return People(dict['id'], dict['name'], dict['age'], dict['sex'])


def test_json_obj(obj):
    str = json.dumps(obj, default=people2dict)
    print(str)

    obj_after = json.loads(str, object_hook=dict2people)
    print(obj_after)



# testing
if __name__ == '__main__':
    d = dict(name='cent', sex='M', age=20)
    print('test pickle: ')
    test_pickle(d)

    print('test json: ')
    test_json(d)

    print('test json any obj: ')
    test_json_obj(People(1, 'cent', 20, 'M'))