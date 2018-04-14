# *_* coding: utf-8 *_*

import sqlite3
from flask import g, current_app


def connect_db():
    '''
    数据库连接对象 rv
    '''
    rv = sqlite3.connect(current_app.config['DATABASE_URL'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    '''
    数据库初始化
    '''
    db = get_db()
    with open('db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit
    db.close()


def get_db():
    '''
    程序实例对象创建数据库连接
    '''
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def query_db(query, args=(), one=False):
    '''
    封装通用查询方法

    @query: 查询sql语句
    @args: 查询参数
    @one: true 查询单条结果， False 查询多条
    '''
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(insert, args=()):
    '''
    封装通用查询方法

    @insert: 插入sql语句
    @args: 参数
    '''
    db = get_db()
    try:
        db.execute(insert, args)
    except:
        return False
    db.commit()
    db.close()
    return True
