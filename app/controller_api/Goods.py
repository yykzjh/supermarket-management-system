from flask import Blueprint, request


app_goods = Blueprint("app_goods", __name__)



@app_goods.route("/Index")
def index():
    return "goods index"





