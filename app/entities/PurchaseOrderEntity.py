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
    
