'''
Author: yykzjh
Date: 2021-01-04 09:05:59
Description: 供货商实体的方法接口
'''

from sqlalchemy import (or_, func)
from app.models import db, Supplier, to_json


'''
description: 返回所有供应商信息
author: yykzjh
Date: 2021-01-05 21:16:04
param {无}
return {[Supplier]}
'''
def details():
    suppliers = Supplier.query.all()
    return to_json(suppliers)
