from flask import Blueprint, request
from sqlalchemy import (or_, func)

app_history_orders = Blueprint("app_history_orders", __name__)

@app_history_orders.route("/index")
def index():
    return "history orders index"