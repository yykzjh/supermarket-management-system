import os
import base64
import requests
import json
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


def get_access_token(client_id, client_secret):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + \
            '&client_secret=' + client_secret
    response = requests.get(host)
    if response:
        return response.json()['access_token']


'''
description: 用户注册
author: yykzjh
Date: 2021-01-10 11:30:25
param {账号:str} username
param {密码:str} password
param {姓名:str} name
param {性别:str} gender
param {生日:date} birthday
param {电话:str} mobile
param {负责区域:str} area
param {工资:float} salary
param {角色id:int} role_id
param {用户人脸图片:Base64} face
return JSON {StatusCode:200/400, msg:"已有同账号的用户！"/response['error_msg']/"请求失败！"}
'''
@app_users.route("/Register", methods=["POST"])
def register():
    newUser = request.get_json()
    user_id = newUser.get('username')
    user_password = newUser.get("password")
    name = newUser.get('name')
    gender = newUser.get('gender')
    birthday = newUser.get('birthday')
    mobile = newUser.get('mobile')
    area = newUser.get('area')
    salary = newUser.get('salary')
    role_id = newUser.get('role_id')
    user_face = newUser.get('face')
    # 首次请求获取access_token
    access_token = get_access_token("6TxFYc3iYRvqym28qullO4rI", "wh2im6M0fAzpa6PAdyspNLZehLculqxz")
    # 人脸注册请求路由
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
    # 请求头
    headers = {'content-type': 'application/json'}
    # 完整的请求路由
    complete_request_url = request_url + "?access_token=" + access_token
    # 请求体中的请求参数
    params = {
        'image':user_face,
        'image_type':'BASE64',
        'group_id':'admin',
        'user_id':user_id,
        'user_info':user_password,
        'quality_control':'NORMAL',
        'liveness_control':'NORMAL'
    }
    params = json.dumps(params)
    # 发送人脸注册请求
    response = requests.post(complete_request_url, data=params, headers=headers)
    # 返回信息处理
    if response:
        response = response.json()
        if response['error_code'] == 0 and response['error_msg'] == 'SUCCESS':
            if addUser(user_id, user_password, name=name, gender=gender, birthday=birthday, mobile=mobile,
                area=area, salary=salary, role_id=role_id):
                return jsonify(StatusCode=200)
            else:
                return jsonify(StatusCode=400, msg="已有同账号的用户！")
        else:
            return jsonify(StatusCode=400, msg=response['error_msg'])
    return jsonify(StatusCode=400, msg="请求失败！")


'''
description: 人脸识别登录
author: yykzjh
Date: 2021-01-10 12:10:35
param {人脸:Base64} face
return {StatusCode:200/400, token, role_id, msg:"没有找到匹配的用户！"/response['error_msg']/"请求失败！"}
'''
@app_users.route("/FaceLogin", methods=["POST"])
def faceLogin():
    user_info = request.get_json()
    user_face = user_info.get('face')
    # 首次请求获取access_token
    access_token = get_access_token("6TxFYc3iYRvqym28qullO4rI", "wh2im6M0fAzpa6PAdyspNLZehLculqxz")
    # 人脸搜索请求路由
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    # 请求头faceLogin
    headers = {'content-type': 'application/json'}
    # 完整的请求路由
    complete_request_url = request_url + "?access_token=" + access_token
    # 请求体中的请求参数
    params = {
        'image':user_face,
        'image_type':'BASE64',
        'group_id_list':'admin',
        'quality_control':'LOW',
        'liveness_control':'NORMAL'
    }
    params = json.dumps(params)
    # 发送人脸搜索请求
    response = requests.post(complete_request_url, data=params, headers=headers)
    if response:
        response = response.json()
        print(response)
        user = response['result']['user_list'][0]
        if response['error_code'] == 0 and response['error_msg'] == 'SUCCESS':
            if user['score'] > 80:
                token =base64.b64encode(os.urandom(24)).decode('utf-8')
                session["token"] = token
                user = select(user['user_id'], user['user_info'])
                if user != None:
                    return jsonify(StatusCode=200, token=token, role_id=user.get('role_id'))
            return jsonify(StatusCode=400, msg="没有找到匹配的用户！")
        else:
            return jsonify(StatusCode=400, msg=response['error_msg'])
    else:
        return jsonify(StatusCode=400, msg="请求失败！")
    
    
    
