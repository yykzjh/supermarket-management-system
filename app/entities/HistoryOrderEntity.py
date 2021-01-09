'''
Author: yykzjh
Date: 2021-01-04 09:03:55
Description: 历史售出记录实体的方法接口
'''

from sqlalchemy import (or_, func, and_)
from app.models import db, Order, to_json, Category


'''
description: 查询指定时间段和商品列表的收益
author: yykzjh
Date: 2021-01-06 15:20:38
param {开始时间:datetime} startTime
param {结束时间:datetime} endTime
param {商品列表:[int]} goods
return {支出:float}
'''
def revenueInPeriod(startTime, endTime, goods):
    records = Order.query.filter(and_(Order.good_id.in_(goods), \
                    Order.datetime>=startTime, Order.datetime<endTime)).all()
    
    sum = 0.0
    for record in records:
        sum += record.amount * record.price
    
    return sum



def addOrder(good_id, supplier_id, price, amount, datetime, id=0):
    newOrder = []
    if id != 0:
        newOrder = Order(id=id, good_id=good_id, supplier_id=supplier_id, \
                        price=price, amount=amount, datetime=datetime)
    else:
        newOrder = Order(good_id=good_id, supplier_id=supplier_id, \
                        price=price, amount=amount, datetime=datetime)
    
    db.session.add(newOrder)
    db.session.commit()
    return newOrder.id


def deleteOrder(order_id):
    orders = Order.query.filter_by(id=order_id).all()
    if len(orders) == 0:
        return False
    else:
        for order in orders:
            db.session.delete(order)
        db.session.commit()
        return True


def selectOrders():
    orders = to_json(Order.query.all())
    for order in orders:
        order['good_name'] = Category.query.get(order['good_id']).name
    return orders


def selectPriceList(start_time, end_time, good_id):
    orders = Order.query.filter(and_(Order.good_id==good_id,
        Order.datetime>=start_time, Order.datetime<end_time)).all()
    
    priceList = []
    for order in orders:
        priceList.append(dict(datetime=order.datetime, price=order.price))
    return priceList
