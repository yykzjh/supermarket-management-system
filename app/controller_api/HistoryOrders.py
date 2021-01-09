from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchGoodsId, goodIdToName, topCats
from app.entities.HistoryOrderEntity import (revenueInPeriod, selectOrders, deleteOrder, selectPriceList,
    goodSaleAmountInPeriod, goodsCountInPeriod)
import datetime
from dateutil.relativedelta import relativedelta


app_history_orders = Blueprint("app_history_orders", __name__)


@app_history_orders.route("/Index")
def index():
    return "history orders index"


'''
description: 根据提供的时间段、划分单位和划分长度、商品类别id，返回分段的收益数据
author: yykzjh
Date: 2021-01-06 15:24:55
param {开始时间:datetime} startTime
param {结束时间:datetime} endTime
param {分段单位:'year'/'month'/'day'/'hour'} unit
param {分段的长度:int} timeLength
param {类别id:int} catId
return JSON {results:[dict]} dict:{startTime, endTime, revenue}
'''
@app_history_orders.route("/RevenueOfDivideTime", methods=["POST"])
def revenueOfDivideTime():
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
        aPeriod['revenue'] = revenueInPeriod(current_start, current_end, allGoodsId)
        results.append(aPeriod)
        #改变循环条件
        current_start += delta
        current_end = current_start + delta
    
    return jsonify(results=results)



'''
description: 以购买人次为一行返回历史订单
author: yykzjh
Date: 2021-01-08 17:39:36
param {无}
return {orders:dict} dict:{int(order_id):{good_name, price, amount, datetime}}
'''
@app_history_orders.route("/AllHistoryOrders", methods=["GET"])
def showHistoryOrders():
    orders = selectOrders()
    
    data = dict()
    for order in orders: # 修改数据格式
        data[order['id']] = data.setdefault(order['id'], dict(good_name="", price="", amount="", datetime=order['datetime'].strftime('%Y-%m-%d %H:%M:%S')))
        data[order['id']]['good_name'] = data[order['id']]['good_name'] + "  " + order['good_name']
        data[order['id']]['price'] = data[order['id']]['price'] + "  " + str(order['price'])
        data[order['id']]['amount'] = data[order['id']]['amount'] + "  " + str(order['amount'])
    
    #去掉字符串最前面的空格
    for value in data.values():
        value['good_name'] = value['good_name'].lstrip()
        value['price'] = value['price'].lstrip()
        value['amount'] = value['amount'].lstrip()

    return jsonify(orders=data)


'''
description: 删除指定编号的订单
author: yykzjh
Date: 2021-01-08 17:46:38
param {订单id:int} order_id
return JSON {StatusCode:200/400, msg:"没有该订单！"}
'''
@app_history_orders.route("/DeleteHistoryOrder", methods=["GET"])
def deleteHistoryOrder():
    order_id = request.args.get('order_id')
    if deleteOrder(order_id):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400, msg="没有该订单！")


'''
description: 返回某件商品一段时间内的售价变化数组
author: yykzjh
Date: 2021-01-09 17:19:27
param {商品id:int} good_id
param {起始时间:datetime} start_time
param {终止时间:datetime} end_time
return {priceList:[dict]} dict:{datetime, price}
'''
@app_history_orders.route("/GoodSalePriceInPeriod", methods=["POST"])
def goodSalePriceInPeriod():
    info = request.get_json()
    good_id = info.get('good_id')
    start_time = info.get('start_time')
    end_time = info.get('end_time')

    priceList = selectPriceList(start_time, end_time, good_id)
    return jsonify(priceList=priceList)


'''
description: 返回一定时间内指定分类下所有商品的销量
author: yykzjh
Date: 2021-01-09 17:44:57
param {分类id:int} catId
param {起始时间:datetime} start_time
param {终止时间:datetime} end_time
return {saleAmountList:[dict]} dict:{name, value}
'''
@app_history_orders.route("/GoodsSaleAmountInPeriod", methods=["POST"])
def goodsSaleAmountInPeriod():
    info = request.get_json()
    catId = info.get('catId')
    start_time = info.get('start_time')
    end_time = info.get('end_time')
    goodsId = searchGoodsId(catId)

    saleAmountList = []
    for goodId in goodsId:
        saleAmountInPeriod.append(dict(name=goodIdToName(goodId), 
            value=goodSaleAmountInPeriod(goodId, start_time, end_time)))
    
    return jsonify(saleAmountList=saleAmountList)


'''
description: 以月为单位返回前六个月各顶级分类的购买次数
author: yykzjh
Date: 2021-01-09 19:00:43
param {无}
return JSON {data:[dict]} dict:{catId, name, data:[dict2]} dict2:{start_time, end_time, count}
'''
@app_history_orders.route("/TopCatsSaleCount", methods=["GET"])
def topCatsSaleCount():
    Cats = topCats()

    data = []
    now_time = datetime.datetime.now()
    delta = relativedelta(months=+1)
    for topCat in Cats:
        tmpDict = dict(catId=topCat['id'], name=topCat['name'], data=[])
        goods = searchGoodsId(topCat['id'])
        date_time = now_time
        for i in range(6):
            tmpMonth = dict(start_time=date_time.strftime('%Y-%m-%d %H:%M:%S'), 
                end_time=(date_time-delta).strftime('%Y-%m-%d %H:%M:%S'), 
                count=goodsCountInPeriod(goods, date_time-delta, date_time))
            tmpDict['data'].append(tmpMonth)
            date_time -= delta
        data.append(tmpDict)
    return jsonify(data=data)

