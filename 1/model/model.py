# =================================================
# 数据库中表对应的类
# =================================================

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import json
from flask import request
import requests
from app import db
from flask import session


#
# class Config():
#     """配置参数"""
#     # 设置sqlalchemy自动跟踪数据库
#     DIALECT = 'mysql'
#     DRIVER = 'pymysql'
#     USERNAME = 'root'
#     PASSWORD = '123456'
#     HOST = '127.0.0.1'
#     PORT = '3306'
#     DATABASE = 'bookManage'  # 必须已经存在，空的也没问题
#
#     SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=UTF8MB4'.format(
#         DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
#     )
#     # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_COMMIT_TEARDOWN = True
#     SQLALCHEMY_POOL_SIZE = 10
#     SQLALCHEMY_MAX_OVERFLOW = 5
#

class Administrator(db.Model):
    __tablename__ = "Administrator"
    AID = db.Column(db.String(4), primary_key=True, nullable=False)
    Aname = db.Column(db.Text(20), nullable=False)
    Apwd = db.Column(db.String(150), nullable=False)


class Reader(db.Model):
    __tablename__ = "Reader"
    RID = db.Column(db.String(4), primary_key=True, nullable=False)
    Rname = db.Column(db.Text(20), nullable=False)
    Rtel = db.Column(db.String(11), nullable=False)
    Rem = db.Column(db.String(40), nullable=False)
    Rpwd = db.Column(db.String(150), nullable=False)



class PBook(db.Model):
    __tablename__ = "PBook"
    ISBN = db.Column(db.String(10), primary_key=True, nullable=False)
    Bname = db.Column(db.Text(20), nullable=False)
    Author = db.Column(db.Text(50), nullable=False)
    Pub = db.Column(db.Text(20), nullable=False)
    Pyear = db.Column(db.Date, nullable=False)
    num = db.Column(db.Integer, nullable=False)
    Per = db.Column(db.Text(20), nullable=False)


class Book(db.Model):
    __tablename__ = "Book"
    BID = db.Column(db.String(4), primary_key=True, nullable=False)
    ISBN = db.Column(db.String(10), db.ForeignKey('PBook.ISBN'), nullable=False)
    Loc = db.Column(db.Text(30), nullable=False)
    Sta = db.Column(db.String(10), default='未借出', nullable=False)
    Per = db.Column(db.Text(20), nullable=False)
    # 非属性
    PBook_ISBN = db.relationship('PBook', backref=db.backref('PBook_ISBN'))  # Reader_BR没用的


class BR_list(db.Model):
    __tablename__ = "BR_list"
    RID = db.Column(db.String(4), db.ForeignKey('Reader.RID'), primary_key=True, nullable=False)
    BID = db.Column(db.String(4), db.ForeignKey('Book.BID'), primary_key=True, nullable=False)
    # 时间默认
    Botime = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False, primary_key=True)
    Rbtime1 = db.Column(db.DateTime, default=datetime.datetime.now() + datetime.timedelta(days=25), nullable=False)
    Rbtime2 = db.Column(db.DateTime, nullable=True)
    Penalty = db.Column(db.Integer, default=0, nullable=True)
    # 非属性
    Reader_BR = db.relationship('Reader', backref=db.backref('Reader_BR'))  #
    Book_BR = db.relationship('Book', backref=db.backref('Book_BR'))  #
    # PBook_BR = db.relationship('PBook', backref=db.backref('PBook_BR'))  #


class R_list(db.Model):
    __tablename__ = "R_list"
    RID = db.Column(db.String(4), db.ForeignKey('Reader.RID'), primary_key=True, nullable=False)
    BID = db.Column(db.String(4), db.ForeignKey('Book.BID'), primary_key=True, nullable=False)
    Status = db.Column(db.Boolean, default=False, nullable=False)
    Aptime1 = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    Aptime2 = db.Column(db.DateTime, default=datetime.datetime.now() + datetime.timedelta(days=10), nullable=False)
    # 非属性
    Reader_R = db.relationship('Reader', backref=db.backref('Reader_R'))  # 没用的
    # PBook_R = db.relationship('PBook', backref=db.backref('PBook_R'))  # 没用的


class R_sta(db.Model):
    __tablename__ = "R_sta"
    RID = db.Column(db.String(4), db.ForeignKey('Reader.RID'), primary_key=True, nullable=False)
    Normal = db.Column(db.Boolean, default=True, nullable=False)
    Remark = db.Column(db.Integer, default=0, nullable=False)
    # 非属性
    Reader_Sta = db.relationship('Reader', backref=db.backref('Reader_Sta'))  # 没用的


class Remark_set(db.Model):
    __tablename__ = "Remark_set"
    REID = db.Column(db.Integer, primary_key=True, nullable=False)
    REname = db.Column(db.Text(30), nullable=False)


class Setting_set(db.Model):
    __tablename__ = "Setting_set"
    SEID = db.Column(db.Integer, primary_key=True, nullable=False)
    SEname = db.Column(db.Text(30), nullable=False)
    SEvalue = db.Column(db.Float, nullable=False)
