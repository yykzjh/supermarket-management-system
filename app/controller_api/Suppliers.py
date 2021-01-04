from flask import Blueprint, request


app_suppliers = Blueprint("app_suppliers", __name__)



@app_suppliers.route("/Index")
def index():
    return "suppliers index"