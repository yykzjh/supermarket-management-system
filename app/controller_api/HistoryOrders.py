from flask import Blueprint, request


app_history_orders = Blueprint("app_history_orders", __name__)


@app_history_orders.route("/Index")
def index():
    return "history orders index"



