from flask import Blueprint, request
from sqlalchemy import (or_, func)
from app.models import db, Role


app_users = Blueprint("app_users", __name__)



@app_users.route("/Login", methods=["GET"])
def login():
    return "login success"


'''
Description: 测试能访问数据库
Author: yykzjh
Date: 2021-01-03 21:59:40
Param: 
Return: 
'''
@app_users.route("/NewRole")
def addRole():
    newRole = Role(name="superadmin")
    db.session.add(newRole)
    db.session.commit()

    return "添加新角色成功！"


