from flask import Blueprint, request, jsonify
from app.entities.StockEntity import details, amountOfGoods
from app.entities.GoodEntity import searchGoodsId


app_stocks = Blueprint("app_stocks", __name__)


@app_stocks.route("/Index")
def index():
    return "stocks index"


'''
description: 返回所有库存记录
author: yykzjh
Date: 2021-01-09 16:47:54
param {无}
return {stocks:[dict]} dict:{good_id, good_name, supplier_id, amount}
'''
@app_stocks.route("/AllStocks", methods=["GET"])
def allStocks():
    stocks = details()
    return jsonify(stocks=stocks)


'''
description: 返回指定分类下所有商品的库存，直接指定商品也可以用
author: yykzjh
Date: 2021-01-09 16:58:05
param {分类id:int} catId
return {amount:float}
'''
@app_stocks.route("/amountOfTheCat", methods=["GET"])
def amountOFTheCat():
    catId = request.args.get('catId')
    goodsId = searchGoodsId(catId)

    amount = amountOfGoods(goodsId)
    return jsonify(amount=amount)
