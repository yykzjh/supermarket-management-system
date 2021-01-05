'''
Author: yykzjh
Date: 2021-01-04 09:05:59
Description: 供货商实体的方法接口
'''

from sqlalchemy import (or_, func)
from app.models import db, Supplier


def details():
    suppliers = Supplier.query.all()
