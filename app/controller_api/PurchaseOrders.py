from flask import Blueprint, request


app_purchase_orders = Blueprint("app_purchase_orders", __name__)


@app_purchase_orders.route("/Index")
def index():
    return "purchase orders index"

