from flask import Blueprint, request


app_stocks = Blueprint("app_stocks", __name__)


@app_stocks.route("/Index")
def index():
    return "stocks index"

