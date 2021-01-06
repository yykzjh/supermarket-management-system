from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchGoodsId


app_goods = Blueprint("app_goods", __name__)



@app_goods.route("/Index")
def index():
    return "goods index"


'''
description: 查询指定分类下所有商品id
author: yykzjh
Date: 2021-01-06 10:16:48
param {分类id:int} catId
return JSON {StatusCode:200/400, allGoods=[int]}
'''
@app_goods.route("/TheCatAllGoods", methods=["GET"])
def theCatAllGoods():
    catId = int(request.args.get('catId'))
    allGoods = searchGoodsId(catId)
    
    if len(allGoods) == 0:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=200, allGoods=allGoods)





