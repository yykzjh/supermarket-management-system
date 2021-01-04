from flask import Blueprint, request


app_statistic = Blueprint("app_statistic", __name__)


@app_statistic.route("/Index")
def index():
    return "statistic index"