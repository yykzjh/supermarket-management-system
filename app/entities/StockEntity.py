'''
Author: yykzjh
Date: 2021-01-04 09:05:30
Description: 库存商品的方法接口
'''

from sqlalchemy import (or_, func)
from app.models import db, Stock, to_json, Good


def details():
    stocks = to_json(Stock.query.all())
    for stock in stocks:
        stock['good_name'] = Good.query.get(stock['good_id']).name
    return stocks


def amountOfGoods(goodsId):
    stocks = Stock.query.filter(Stock.good_id.in_(goodsId)).all()
    sum = 0.0
    for stock in stocks:
        sum += stock.amount
    return sum
