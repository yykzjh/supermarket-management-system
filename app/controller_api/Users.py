from flask import Blueprint, request
from sqlalchemy import (or_, func)

app_users = Blueprint("app_users", __name__)

@app_users.route("/Login", methods=["GET"])
def login():
    return "login success"