#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo  to customize a class with meta-class, 
and a sample to define a simple ORM (Object Relational Mapping) framework with meta-class
元类定制类的例子，及
使用元类定义简单ORM框架，
对象-关系映射（ORM）：数据库表一行记录映射为一个对象，类对应表

use ORM like this:
class User(object):
    id = IntegerField('id')
    name = StringField('name')
    email = StringField('email')
    password = StringField('password')

# create an object    
usr = User(id=1, name='cent', email='cent@cent.com', password='***')
# insert a record into a table 
usr.save()

'''

# define a meta-class to customize Mylist class
# meta-class just like a template of class
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 定制类，绑定属性及方法
        attrs['__name'] = name
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)

# metaclass means Mylist created by ListMetaclass
class Mylist(list, metaclass=ListMetaclass):
    pass

# testing:
mylist = Mylist()
mylist.add('cent')
mylist.add('lina')
print(mylist.__name)
print(mylist)



# define an ORM framework with meta-class
# meta-class is a template of class while class is a template of object

# Field class map to column in database
class Field(object):
    def __init__(self, column_name=None, column_type=None):
        self.__column_name = column_name
        self.__column_type = column_type

    @property
    def column_name(self):
        return self.__column_name

    @property
    def column_type(self):
        return self.__column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.column_name)

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, column_type='bigint')

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, column_type='varchar(100)')


# the metaclass controls the behaviour of class Model
# 动态控制Model类的属性
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 排除对Model类修改
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        # 属性列字段信息映射关系
        mappings = dict()
        for k,v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v

        # 删除同名类属性，避免与对象实例属性冲突(注意：实例属性会覆盖类属性)
        for k in mappings:
            attrs.pop(k)

        attrs['__table__'] = name # 保存表名，默认为类名
        attrs['__mappings__'] = mappings # 保存属性字段映射关系
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    # override to get key-value like attribute
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(r'Model object has no attribute %s' % item)

    # override to set key-value like attribute
    def __setattr__(self, key, value):
        self[key] = value

    # 根据属性字段映射关系，解析构造SQL语句，插入数据库表，即可对象映射为表行记录
    def save(self):
        fields = list()
        params = list()
        args = list()

        for k,v in self.__mappings__.items():
            fields.append(v.column_name)
            params.append('?')
            args.append(getattr(self, k, None)) #获取构造对象的属性值，要求对象定义属性与类属性同名才能映射表列值

        # 构造SQL插入语句
        sql = 'Insert into %s(%s) values(%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: ', sql)
        print('ARGS: ', args)


# inherit from Model, class User will be controlled by ModelMetaclass
class User(Model):
    # define class attributes to map column of table
    id = IntegerField('user_id')
    name = StringField('user_name')
    phone_number = IntegerField('phone_number')
    password = StringField('password')

# inherit from Model, class Blog will be also controlled by ModelMetaclass
class Blog(Model):
    # define class attributes to map column of table
    id = IntegerField('blog_id')
    title = StringField('blog_title')
    content = StringField('blog_content')
    type = StringField('blog_type')
    date = IntegerField('create_date')

if __name__ == '__main__':
    user = User(id=1, name='cent', phone_number=12345678912, password='***')
    user.save()

    blog = Blog(id=1, title='hello world', content='Hello World!!!', type='essay', date=20170610)
    blog.save()

    blog1 = Blog(id=1, title='test', content='test content', date=20170610)
    blog1.save()