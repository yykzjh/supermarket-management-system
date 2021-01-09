from flask import Blueprint, request, jsonify
from app.entities.OnSaleEntity import details, amountOfGoods
from app.entities.GoodEntity import searchGoodsId


app_on_sales = Blueprint("app_on_sales", __name__)


@app_on_sales.route("/Index")
def index():
    return "on sales index"


'''
description: 返回所有上架记录
author: yykzjh
Date: 2021-01-09 17:04:35
param {无}
return {sales:[dict]} dict:{good_id, good_name, supplier_id, amount, price_out}
'''
@app_on_sales.route("/AllSales", methods=["GET"])
def allSales():
    sales = details()
    return jsonify(sales=sales)


'''
description: 返回指定分类下所有商品的上架数量，直接指定商品也可以用
author: yykzjh
Date: 2021-01-09 17:06:23
param {caId}
return {amount:flloat}
'''
@app_on_sales.route("/amountOfTheCat", methods=["GET"])
def amountOFTheCat():
    catId = request.args.get('catId')
    goodsId = searchGoodsId(catId)

    amount = amountOfGoods(goodsId)
    return jsonify(amount=amount)