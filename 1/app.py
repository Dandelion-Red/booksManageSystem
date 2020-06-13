from flask import Flask, render_template,redirect
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
import os


def dbconfig(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/bookmanage?charset=UTF8MB4'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/bookmanage?characterEncoding=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    return SQLAlchemy(app=app)  # 这就是db


app = Flask(__name__)
db = dbconfig(app)
CORS(app, supports_credentials=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# #
# # @app.context_processor
# # def getUser():
# #     from dboperation.dboperation import queryAccordingToID
# #     user = queryAccordingToID('administrator', '1000')
# #     return dict(username=user.Aname)
#
import index
#
#
# 以上是有用信息
# ===========================================================================================================
# /app.py
# !/usr/bin/env python
# encoding: utf-8
# from flask import Flask, render_template, redirect

# app = Flask(__name__)

#
# @app.route('/')
# def index():
#     return render_template('index.html')

#
# @app.route('/__webpack_hmr')
# def npm():
#     return redirect('http://localhost:8080/__webpack_hmr')


if __name__ == '__main__':
    app.run(debug=True)
