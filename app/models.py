from app.config import app
from flask_sqlalchemy import SQLAlchemy

#创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class role(db.Model):
    """用户角色/身份表"""
    __tablename__ = "sms_roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    users = db.relationship("User",backref="role")


class User(db.Model):
    """用户表"""
    __tablename__ = "sms_users" # 指明数据库的表名

    id = db.Column(db.String(10), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(4), nullable=False)
    gender = db.Column(db.String(1))
    birthday = db.Column(db.Date)
    mobile = db.Column(db.String(11))
    area = db.Column(db.String(128))
    salary = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey("sms_roles.id"))

