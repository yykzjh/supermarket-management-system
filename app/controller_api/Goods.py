from flask import Blueprint, request
from sqlalchemy import (or_, func)

app_goods = Blueprint("app_goods", __name__)

@app_goods.route("/index")
def index():
    return "goods index"