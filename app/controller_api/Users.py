from flask import Blueprint, request


app_users = Blueprint("app_users", __name__)



@app_users.route("/Login")
def login():
    return "login success"


