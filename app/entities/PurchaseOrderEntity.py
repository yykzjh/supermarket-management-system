'''
Author: yykzjh
Date: 2021-01-04 09:05:21
Description: 进货记录的方法接口
'''

from sqlalchemy import (or_, func, and_)
from app.models import db, Purchase, to_json


'''
description: 查询指定时间段和商品列表的支出
author: yykzjh
Date: 2021-01-06 10:54:59
param {开始时间:datetime} startTime
param {结束时间:datetime} endTime
param {商品列表:[int]} goods
return {支出:float}
'''
def expenditureInPeriod(startTime, endTime, goods):
    records = Purchase.query.filter(and_(Purchase.good_id.in_(goods), Purchase.if_finish==True, \
        Purchase.finishtime>=startTime, Purchase.finishtime<endTime)).all()
    
    sum = 0.0
    for record in records:
        sum += record.amount * record.price_in
    
    return sum


def details():
    purchaseOrders = to_json(Purchase.query.all())
    for purchaseOrder in purchaseOrders:
        purchaseOrder['good_name'] = Category.query.get(purchaseOrder['good_id']).name
    return purchaseOrders


def finishPurchaseOrder(good_id, supplier_id, build_time):
    order = Purchase.query.filter_by(good_id=good_id, supplier_id=supplier_id, build_time=build_time).first()
    if order == None:
        return 0
    elif order.if_finish == True:
        return 1
    else:
        order.if_finish = True
        db.session.commit()
        return 2


def selectlimitOrders(goodsId):
    purchaseOrders = to_json(Purchase.query.filter(Purchase.good_id.in_(goodsId)).all())
    for purchaseOrder in purchaseOrders:
        purchaseOrder['good_name'] = Category.query.get(purchaseOrder['good_id']).name
    return purchaseOrders


def selectPriceList(start_time, end_time, good_id):
    orders = Purchase.query.filter(and_(Purchase.good_id==good_id, Purchase.if_finish==True,
        Purchase.finishtime>=start_time, Purchase.finishtime<end_time)).all()
    
    priceList = []
    for order in orders:
        priceList.append(dict(finish_time=order.finishtime, price_in=order.price_in))
    return priceList
    
