from flask import Blueprint, request


app_on_sales = Blueprint("app_on_sales", __name__)


@app_on_sales.route("/Index")
def index():
    return "on sales index"