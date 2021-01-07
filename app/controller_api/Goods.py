from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchGoodsId, categoryDetails, goodDetail


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


'''
description: 返回所有商品类别详细信息的结构树
author: yykzjh
Date: 2021-01-06 16:16:08
param {无}
return {[dict]} results dict:{id, name, parent, level, children:[dict]}
'''
@app_goods.route("/AllCatDetails", methods=["GET"])
def allCatDetails():
    return jsonify(results=categoryDetails(0))


'''
description: 返回指定商品的详细信息
author: yykzjh
Date: 2021-01-07 15:16:29
param {商品id:int} good_id
return JSON {StatusCode:200/400, good:Good}
'''
@app_goods.route("/GoodDetail", methods=["GET"])
def getGoodDetail():
    good_id = request.args.get('good_id')
    good = goodDetail(good_id)
    if good == None:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=200, good=good)




