#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo about ORM framework SQLAlchemy.
ORM: Object-Relational Mapping
'''

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 实现ORM映射基类
Base = declarative_base()

# 继承基类后可映射数据库表
class User(Base):
    # 必须包含此属性给出表名
    __tablename__ = 'user'

    # 定义列名称及类型等属性，必须明确主键
    id = Column(Integer, primary_key=True)
    # nullable设置是否可空，index使用该列创建索引
    name = Column(String(32), nullable=False, index=True)

    # one to many: relative to table 'project'
    project = relationship('Project', back_populates='user')


# 继承基类后可映射数据库表
class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    descript = Column(String(64))

    # foreign key: relative to table 'user'，外键约束，并设置ondelete='CASCADE'以支持联动删除
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    # many to one: relative to table 'user'
    user = relationship('User', back_populates='project')


def test_orm():
    # 初始化数据库连接引擎，格式为'数据库类型+数据库驱动名称://用户名:密码@机器地址:端口/数据库名称'
    engine = create_engine('mysql+mysqlconnector://root:******@localhost:3306/test_orm')

    # 建表指令
    Base.metadata.create_all(engine)

    # 关联数据库连接引擎，创建DB_session工厂类
    DB_session = sessionmaker(bind=engine)

    # 创建会话对象，从engine维护的连接池中获取数据库的一个连接
    session = DB_session()

    print('Test insert:')

    # 创建user对象，映射数据库记录
    new_user = User(id=1, name='cent')
    new_user.project = [Project(id=1, name='javascript', descript='jsp work'),
                        Project(id=2, name='css3', descript='css3 work'),
                        Project(id=3, name='html5', descript='html5 work')]

                         # 通过session操作数据库，pending记录
    session.add(new_user)

    # 提交事务，flush所有pending到数据库
    session.commit()

    # 注意此处修改session会记录下来，ORM identity map保证session中记录与python对象为同一个
    new_user.name = 'lina'
    session.commit()

    # 一次写入多条记录
    session.add_all([User(id=2, name='cent'),
                     User(id=3, name='hello'),
                     User(id=4, name='world')])
    session.commit()
    print('Insert successfully')

    print('Test query:')
    # 获取Query，filter/filter_by为筛选条件，first()返回最多一个结果，one()返回唯一记录（少或多报错），all()返回所有记录
    find_user = session.query(User).filter(User.name == 'world').first()
    if find_user:
        print('find user: %s' % find_user.name)

    print('Test update:')
    if find_user:
        # query返回记录对象，可直接使用对象属性赋值修改
        find_user.name = 'python'
        session.commit()

    # update()更新query返回记录
    session.query(User).filter_by(name='hello').update({'name': 'hi'})
    session.commit()
    print('Update successfully')

    for row in session.query(User).order_by(User.id):
        print(row.id, row.name)

    print('Test Delete:')
    # 删除query返回记录对象
    if find_user:
        session.delete(find_user)
        session.commit()
        print('Delete record %s' % find_user.name)


    find_project = session.query(Project).join(User).filter(User.name=='lina').all()
    for row in find_project:
        print(row.name)

    # 删除所有记录
    session.query(User).delete()
    session.commit()
    print('Delete all record')

    # 最后关闭会话
    session.close()


# todo some test
if __name__ == '__main__':
    test_orm()
