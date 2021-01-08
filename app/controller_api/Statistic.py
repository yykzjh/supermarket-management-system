from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchNextCatId, theCatFixProfit
from app.entities.PurchaseOrderEntity import expenditureInPeriod
from app.entities.HistoryOrderEntity import revenueInPeriod



app_statistic = Blueprint("app_statistic", __name__)


@app_statistic.route("/Index")
def index():
    return "statistic index"


'''
description: 计算指定分类下前一天、前一月、前一年的利润
author: yykzjh
Date: 2021-01-08 19:46:22
param {类别id:int} catId
return JSON {StatusCode:200/400, data:[dict], msg:"该分类下没有子分类！"} 
            dict:{id, name, parent, level, day_profit, month_profit, year_profit}
'''
@app_statistic.route("/NextCatsProfits", methods=["GET"])
def nextCatsProfits():
    catId = request.args.get('catId')
    # 初始化返回的数据
    data = []
    # 获取下级分类id列表
    nextCatsId = searchNextCatId(catId)
    if len(nextCatsId) == 0:
        return jsonify(StatusCode=400, msg="该分类下没有子分类！")
    # 分别求出利润
    for nextId in nextCatsId:
        data.append(theCatFixProfit(nextId))
    return jsonify(StatusCode=200, data=data)
    



