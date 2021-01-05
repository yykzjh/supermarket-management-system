from flask import Blueprint, request, jsonify, session
from app.entities.SupplierEntity import details


app_suppliers = Blueprint("app_suppliers", __name__)



@app_suppliers.route("/Index")
def index():
    return "suppliers index"


'''
description: 返回所有供应商信息
author: yykzjh
Date: 2021-01-05 21:20:10
param {无}
return JSON {StatusCode:200/400, suppliers:[Supplier]}
'''
@app_suppliers.route("/SuppliersInfo", methods=["GET"])
def allSuppliers():
    suppliers = details()

    if suppliers == None:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=400, suppliers=suppliers)