from flask import Blueprint, request
from sqlalchemy import (or_, func)
from app.models import db


app_goods = Blueprint("app_goods", __name__)



@app_goods.route("/Index")
def index():
    return "goods index"





