'''
Author: yykzjh
Date: 2021-01-04 09:03:55
Description: 历史售出记录实体的方法接口
'''

from sqlalchemy import (or_, func, and_)
from app.models import db, Order, to_json


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
