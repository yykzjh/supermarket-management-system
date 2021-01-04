from flask import Blueprint, request, jsonify
from app.entities.UserEntity import select


app_users = Blueprint("app_users", __name__)


'''
Description: 登录接口 POST /Users/Login
Author: yykzjh
Date: 2021-01-04 13:33:20
Param: JSON {id:str, password:str}
Return: JSON {StatusCode:200/400}
'''
@app_users.route("/Login",methods=["POST"])
def login():
    user = request.get_json()
    user_id = user.get('id')
    user_pwd = user.get('password')

    if select(user_id, user_pwd):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400)



