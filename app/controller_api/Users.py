import os
import base64
from flask import Blueprint, request, jsonify, session
from app.entities.UserEntity import (select, addUser, deleteUser, details, detail, updateUser)


app_users = Blueprint("app_users", __name__)


'''
Description: 登录接口 POST /Users/Login
Author: yykzjh
Date: 2021-01-04 13:33:20
Param: JSON {username:str, password:str}
Return: JSON {StatusCode:200/400, token:str, role_id:int}
'''
@app_users.route("/Login", methods=["POST"])
def login():
    user = request.get_json()
    user_id = user.get('username')
    user_pwd = user.get('password')

    token =base64.b64encode(os.urandom(24)).decode('utf-8')
    session["token"] = token

    user = select(user_id, user_pwd)

    if user != None:
        return jsonify(StatusCode=200, token=token, role_id=user.get('role_id'))
    else:
        return jsonify(StatusCode=400)


'''
description: 返回指定角色名的所有用户信息
author: yykzjh
Date: 2021-01-05 19:18:23
param {角色的名字:str} name
return JSON {StatusCode:200/400, users:[User]}
'''
@app_users.route("/AllUsers", methods=["GET"])
def allUsers():
    role_name = request.args.get('name')
    print(role_name)
    users = details(role_name)

    if users == None:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=200, users=users)


'''
description: 返回指定账号的用户信息
author: yykzjh
Date: 2021-01-05 19:19:55
param {账号:str} username
return JSON {StatusCode:200/400, user:User}
'''
@app_users.route("/OneUser", methods=['GET'])
def aUser():
    user_id = request.args.get('username')
    user = detail(user_id)
    
    if user == None:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=200, user=user)


'''
description: 添加新用户
author: yykzjh
Date: 2021-01-05 19:20:42
param {账号:str} username
param {密码:str} password
param {姓名:str} name
param {性别:str} gender
param {生日:date} birthday
param {电话:str} mobile
param {负责区域:str} area
param {工资:float} salary
param {角色id:int} role_id
return JSON {StatusCode:200/400}
'''
@app_users.route("/NewUser", methods=["POST"])
def insert():
    user = request.get_json()
    if addUser(user.get("username"), user.get("password"), user.get('name'), user.get('gender'), user.get('birthday'), \
            user.get('mobile'), user.get('area'), user.get('salary'), user.get('role_id')):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400)


'''
description: 删除指定账号的用户 GET
author: yykzjh
Date: 2021-01-05 19:21:43
param {账号:str} username
return JSON {StatusCode:200/400}
'''
@app_users.route("/RestUser", methods=["GET"])
def delete():
    if deleteUser(request.args.get('username')):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400)


'''
description: 更新指定账号的用户密码
author: yykzjh
Date: 2021-01-05 19:22:21
param {账号:str} username
param {密码:str} password
return JSON {StatusCode:200/400}
'''
@app_users.route("/NewPwd", methods=["POST"])
def updatePwd():
    user = request.get_json()
    user_id = user.get('username')
    user_pwd = user.get('password')

    if updateUser(user_id, password=user_pwd):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400)


'''
description: 更新指定账号的用户角色
author: yykzjh
Date: 2021-01-05 19:22:21
param {账号:str} username
param {角色id:int} role_id
return JSON {StatusCode:200/400}
'''
@app_users.route("/NewRoleId", methods=["POST"])
def updateRoleId():
    user = request.get_json()
    user_id = user.get('username')
    user_role_id = user.get('role_id')

    if updateUser(user_id, role_id=user_role_id):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400)

