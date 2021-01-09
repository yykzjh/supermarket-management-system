from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchGoodsId, goodIdToName
from app.entities.PurchaseOrderEntity import (expenditureInPeriod, details, finishPurchaseOrder, selectlimitOrders,
    selectPriceList, goodPurchaseAmountInPeriod)
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
    cost = expenditureInPeriod(startTime, endTime, allGoodsId)

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
        aPeriod['expenditure'] = expenditureInPeriod(current_start, current_end, allGoodsId)
        results.append(aPeriod)
        #改变循环条件
        current_start += delta
        current_end = current_start + delta
    
    return jsonify(results=results)


'''
description: 返回所有订货订单
author: yykzjh
Date: 2021-01-09 16:12:54
param {无}
return {purchaseOrders:[dict]} dict:{good_id, good_name, supplier_id, build_time, finish_time, if_shelf, if_finish}
'''
@app_purchase_orders.route("/AllPurchaseOrders", methods=["GET"])
def allPurchaseOrders():
    purchaseOrders = details()
    return jsonify(purchaseOrders=purchaseOrders)



'''
description: 修改进货订单状态为已完成
author: yykzjh
Date: 2021-01-09 16:28:34
param {商品id:int} good_id
param {供货商id:int} supplier_id
param {建立订单时间:datetime} build_time
return JSON {StatusCode:200/400, msg:"没有该订单！"/"该订单状态为已完成！"}
'''
@app_purchase_orders.route("/StatusToFinish", methods=["POST"])
def statusToFinish():
    info = request.get_json()
    good_id = info.get('good_id')
    supplier_id = info.get('supplier_id')
    build_time = info.get('build_time')

    flag = finishPurchaseOrder(good_id, supplier_id, build_time)
    if flag == 0:
        return jsonify(StatusCode=400, msg="没有该订单！")
    elif flag == 1:
        return jsonify(StatusCode=400, msg="该订单状态为已完成！")
    else:
        return jsonify(StatusCode=200)
    

'''
description: 返回一个分类id下的所有商品的进货订单
author: yykzjh
Date: 2021-01-09 16:38:01
param {分类id:int} catId
return {orders:[dict]} dict:{good_id, good_name, supplier_id, build_time, finish_time, if_shelf, if_finish}
'''
@app_purchase_orders.route("/CatPurchaseOrders", methods=["GET"])
def catPurchaseOrders():
    catId = request.args.get('catId')
    goodsId = searchGoodsId(catId)

    orders = selectlimitOrders(goodsId)
    return jsonify(orders=orders)


'''
description: 返回某件商品一段时间内的进价变化数组
author: yykzjh
Date: 2021-01-09 17:19:27
param {商品id:int} good_id
param {起始时间:datetime} start_time
param {终止时间:datetime} end_time
return {priceList:[dict]} dict:{finish_time, price_in}
'''
@app_purchase_orders.route("/GoodPurchasePriceInPeriod", methods=["POST"])
def goodPurchasePriceInPeriod():
    info = request.get_json()
    good_id = info.get('good_id')
    start_time = info.get('start_time')
    end_time = info.get('end_time')

    priceList = selectPriceList(start_time, end_time, good_id)
    return jsonify(priceList=priceList)


'''
description: 返回一定时间内指定分类下所有商品的进货数量
author: yykzjh
Date: 2021-01-09 17:44:57
param {分类id:int} catId
param {起始时间:datetime} start_time
param {终止时间:datetime} end_time
return {purchaseAmountList:[dict]} dict:{name, value}
'''
@app_purchase_orders.route("/GoodsPurchaseAmountInPeriod", methods=["POST"])
def goodsPurchaseAmountInPeriod():
    info = request.get_json()
    catId = info.get('catId')
    start_time = info.get('start_time')
    end_time = info.get('end_time')
    goodsId = searchGoodsId(catId)

    purchaseAmountList = []
    for goodId in goodsId:
        purchaseAmountInPeriod.append(dict(name=goodIdToName(goodId), 
            value=goodPurchaseAmountInPeriod(goodId, start_time, end_time)))
    
    return jsonify(purchaseAmountList=purchaseAmountList)
