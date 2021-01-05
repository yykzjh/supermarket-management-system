import os
import base64
from flask import Blueprint, request, jsonify, session
from app.entities.UserEntity import select


app_users = Blueprint("app_users", __name__)


'''
Description: 登录接口 POST /Users/Login
Author: yykzjh
Date: 2021-01-04 13:33:20
Param: JSON {username:str, password:str}
Return: JSON {StatusCode:200/400, token:str}
'''
@app_users.route("/Login",methods=["POST"])
def login():
    user = request.get_json()
    user_id = user.get('username')
    user_pwd = user.get('password')

    token =base64.b64encode(os.urandom(24)).decode('utf-8')
    session["token"] = token


    if select(user_id, user_pwd):
        print(token)
        return jsonify(StatusCode=200, token=token)
    else:
        return jsonify(StatusCode=400)



