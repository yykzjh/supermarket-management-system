# coding:utf-8
from app.controller_api import app

class Config1(object):

    # 开启DEBUG模式
    DEBUG = True

    #设置密钥
    SECRET_KEY = "fjhfdsfhdgsjdsjaffgaj"

    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:sww533212@127.0.0.1:3306/supermarket"
    
    # 设置sqlalchemy自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 设置查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    # 配置文件路径，防止恶意读取文件
    UPLOAD_FOLDER = '/Users/swenw/Desktop/software'

    # 设置上传文件大小
    MAX_CONTENT_LENGTH = 1024 * 1024


app.config.from_object(Config1)


    