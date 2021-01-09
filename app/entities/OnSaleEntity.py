'''
Author: yykzjh
Date: 2021-01-04 09:05:02
Description: 在售商品实体的方法接口
'''

from sqlalchemy import (or_, func)
from app.models import db, Sale, to_json, Good


def details():
    sales = to_json(Sale.query.all())
    for sale in sales:
        sale['good_name'] = Good.query.get(sale['good_id']).name
    return sales


def amountOfGoods(goodsId):
    sales = Sale.query.filter(Sale.good_id.in_(goodsId)).all()
    sum = 0.0
    for sale in sales:
        sum += sale.amount
    return sum