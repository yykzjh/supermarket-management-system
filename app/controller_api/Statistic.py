from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchGoodsId
from app.entities.PurchaseOrderEntity import expenditureInPeriod
from app.entities.HistoryOrderEntity import revenueInPeriod
import datetime
from dateutil.relativedelta import relativedelta


app_statistic = Blueprint("app_statistic", __name__)


@app_statistic.route("/Index")
def index():
    return "statistic index"


'''
description: 计算指定分类下前一天、前一月、前一年的利润
author: yykzjh
Date: 2021-01-08 19:46:22
param {类别id:int} catId
return JSON {day_profit:float, month_profit:float, year_profit:float}
'''
@app_statistic.route("/TheCatFixRevenue", methods=["GET"])
def theCatFixRevenue():
    catId = request.args.get('catId')
    # 获得该分类下所有商品id
    goods = searchGoodsId(catId)
    # 定义时间段
    now_time = datetime.datetime.now()
    before_day = now_time - datetime.timedelta(days=1)
    before_month = now_time - relativedelta(months=+1)
    before_year = now_time - relativedelta(years=+1)
    # 计算不同时间段的利润
    day_profit = revenueInPeriod(before_day, now_time, goods) - expenditureInPeriod(before_day, now_time, goods)
    month_profit = revenueInPeriod(before_month, now_time, goods) - expenditureInPeriod(before_month, now_time, goods)
    year_profit = revenueInPeriod(before_year, now_time, goods) - expenditureInPeriod(before_year, now_time, goods)
    return jsonify(day_profit=day_profit, month_profit=month_profit, year_profit=year_profit)



