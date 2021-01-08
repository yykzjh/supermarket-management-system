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
    if len(suppliers) == 0:
        return None
    else:
        return to_json(suppliers)


def addSupplier(name, mobile, province, city, sign_start, sign_end):
    supplier = Supplier.query.filter_by(name=name, province=province, city=city).first()
    if supplier != None:
        return False

    newSupplier = Supplier(name=name, mobile=mobile, province=province, \
                        city=city, sign_start=sign_start, sign_end=sign_end)
    db.session.add(newSupplier)
    db.session.commit()
    return True


def deleteSupplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if supplier == None:
        return False
    db.session.delete(supplier)
    db.session.commit()
    return True


def updateSupplier(id, name=None, mobile=None, province=None, city=None, sign_start=None, sign_end=None):
    supplier = Supplier.query.get(id)
    if supplier == None:
        return False
    supplier.name = supplier.name if name==None else name
    supplier.mobile = supplier.mobile if mobile==None else mobile
    supplier.province = supplier.province if province==None else province
    supplier.city = supplier.city if city==None else city
    supplier.sign_start = supplier.sign_start if sign_start==None else sign_start
    supplier.sign_end = supplier.sign_end if sign_end==None else sign_end
    db.session.commit()
    return True


def selectSupplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if supplier == None:
        return None
    else:
        return supplier.to_dict()


def divideProvince():
    statisticList = db.session.query(Supplier.province, func.count(Supplier.id).label('value')).\
                                group_by(Supplier.province).all()
    
    suppliersList = []
    for item in statisticList:
        tempItem = dict(name=item.province,value=item.value)
        suppliersList.append(tempItem)
    
    return suppliersList


def divideCity(province):
    statisticList = db.session.query(Supplier.city, func.count(Supplier.id).label('value')).\
                                filter_by(province=province).group_by(Supplier.city).all()
    
    suppliersList = []
    for item in statisticList:
        tempItem = dict(name=item.city,value=item.value)
        suppliersList.append(tempItem)
    
    return suppliersList
    
