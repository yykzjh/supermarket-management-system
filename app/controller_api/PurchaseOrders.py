from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchGoodsId
from app.entities.PurchaseOrderEntity import balanceInPeriod
import datetime
from dateutil.relativedelta import relativedelta


app_purchase_orders = Blueprint("app_purchase_orders", __name__)


@app_purchase_orders.route("/Index")
def index():
    return "purchase orders index"


'''
description: 计算指定时间段和商品分类的支出
author: yykzjh
Date: 2021-01-06 10:56:24
param {开始时间:datetime} startTime
param {结束时间:datetime} endTime
param {分类id:int} catId
return JSON {expenditure:float}
'''
@app_purchase_orders.route("/ExpenditureOfTimeAndCat", methods=["POST"])
def expenditureOfTimeAndCat():
    info = request.get_json()
    startTime = info.get('startTime')
    endTime = info.get('endTime')
    catId = info.get('catId')

    allGoodsId = searchGoodsId(catId)
    cost = balanceInPeriod(startTime, endTime, allGoodsId)

    return jsonify(expenditure=cost)


'''
description: 根据提供的时间段、划分单位和划分长度、商品类别id，返回分段的支出数据
author: yykzjh
Date: 2021-01-06 11:54:06
param {开始时间:datetime} startTime
param {结束时间:datetime} endTime
param {分段单位:'year'/'month'/'day'/'hour'} unit
param {分段的长度:int} timeLength
param {类别id:int} catId
return JSON {results:[dict]} dict:{startTime, endTime, expenditure}
'''
@app_purchase_orders.route("/ExpenditureOfDivideTime", methods=["POST"])
def expenditureOfDivideTime():
    # 解析请求中的数据
    info = request.get_json()
    startTime = datetime.datetime.strptime(info.get('startTime'), '%Y-%m-%d %H:%M:%S') 
    endTime = datetime.datetime.strptime(info.get('endTime'), '%Y-%m-%d %H:%M:%S')
    unit = info.get('unit')
    timeLength = info.get('timeLength')
    catId = info.get('catId')

    # 初始化时间划分的长度单位
    delta = []
    if unit == "year":
        delta = relativedelta(years=+timeLength)
    elif unit == "month":
        delta = relativedelta(months=+timeLength)
    elif unit == "day":
        delta = datetime.timedelta(days=timeLength)
    elif unit == "hour":
        delta = datetime.timedelta(hours=timeLength)
    allGoodsId = searchGoodsId(catId) #获得分类下的商品列表

    # 初始化循环所叙述句
    current_start = startTime
    current_end = startTime + delta
    results = []

    while current_start < endTime:
        # 判断边界时间
        if current_end > endTime:
            current_end = endTime
        # 定义保存一段时间数据的字典
        aPeriod = dict()
        aPeriod['startTime'] = current_start.strftime('%Y-%m-%d %H:%M:%S')
        aPeriod['endTime'] = current_end.strftime('%Y-%m-%d %H:%M:%S')
          # 获取该时间段的支出
        aPeriod['expenditure'] = balanceInPeriod(current_start, current_end, allGoodsId)
        results.append(aPeriod)
        #改变循环条件
        current_start += delta
        current_end = current_start + delta
    
    return jsonify(results=results)
    
