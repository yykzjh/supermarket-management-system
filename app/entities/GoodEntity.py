'''
Author: yykzjh
Date: 2021-01-04 09:03:32
Description: 商品实体的方法接口
'''
import os
from sqlalchemy import (or_, func, not_, and_ ) 
from app.models import db, app, Category, to_json, Good
from app.entities.PurchaseOrderEntity import expenditureInPeriod
from app.entities.HistoryOrderEntity import revenueInPeriod
import datetime
from dateutil.relativedelta import relativedelta


'''
description: 返回指定分类下的所有商品id
author: yykzjh
Date: 2021-01-06 10:15:40
param {分类id:int} cat_id
return {该分类下所有商品id:[int]}
'''
def searchGoodsId(cat_id):
    # 先判断cat_id是不是商品
    originCat = Category.query.get(cat_id)
    if originCat.level == 4:
        return [cat_id]
    
    allGoodsId = []
    allCatId = [cat_id]

    while True:
        preAllCatId = []
        for catId in allCatId:
            lowCatId = Category.query.with_entities(Category.id).filter(and_(Category.parent==catId, not_(Category.level==4))).all()
            lowCatId = [turple[0] for turple in lowCatId]
            preAllCatId.extend(lowCatId)
            lowGoodsId = Category.query.with_entities(Category.id).filter(and_(Category.parent==catId, Category.level==4)).all()
            lowGoodsId = [turple[0] for turple in lowGoodsId]
            allGoodsId.extend(lowGoodsId)
        if preAllCatId:
            allCatId = preAllCatId
        else:
            break
    return allGoodsId


'''
description: 返回指定商品类别下的结构树数据
author: yykzjh
Date: 2021-01-06 16:05:29
param {当前商品的id:int} id
return {[dict]} dict:{id, name, parent, level}
'''
def categoryDetails(id):
    # 查询当前类别的子类别对象列表,并转换成子类型字典列表
    children = to_json(Category.query.filter_by(parent=id).all())
    # 遍历并进行递归
    for child in children:
        if child['level'] < 4:
            child['children'] = categoryDetails(child['id'])
    return children


'''
description: 返回指定商品的信息
author: yykzjh
Date: 2021-01-06 16:15:32
param {商品id:int} good_id
return {Good}
'''
def goodDetail(good_id):
    good = Good.query.get(good_id)
    if good == None:
        return None
    else:
        good = good.to_dict()
        good['name'] = Category.query.get(good_id).name
        return good


'''
description: 新增商品类别
author: yykzjh
Date: 2021-01-07 15:24:46
param {类别名称:str} name
param {新类别所属夫类:int} parent
param {新类别所属的分级层次:int} level
return {新类别自动分配的id:int} 
'''
def addNewCat(name, parent, level):
    # 检测不能添加同名类别
    findCat = Category.query.filter_by(name=name).first()
    if findCat != None:
        return 0

    # 添加新类别
    newCat = Category(name=name, parent=parent, level=level)
    db.session.add(newCat)
    db.session.commit()
    return newCat.id


'''
description: 添加新的商品信息
author: yykzjh
Date: 2021-01-07 16:18:51
param {商品名:str} name
param {商品所属夫类:int} parent
param {商品详细介绍:str} info
param {商品存储地址:str} icon
return {boolean:Ture/False}
'''
def addNewGood(name, parent, intro, icon):
    # 检测不能添加同名商品
    good = Category.query.filter_by(name=name).first()
    if good != None:
        return False

    # 在类别表中新建商品记录
    newCat = Category(name=name, parent=parent, level=4)
    db.session.add(newCat)
    db.session.commit()

    # 在商品表中新建商品记录
    newGood = Good(id=newCat.id, intro=intro, icon=icon)
    db.session.add(newGood)
    db.session.commit()

    return True


def deleteGood(good_id):
    theGood = Good.query.get(good_id)
    if theGood == None:
        return False
    else:
        theCat = Category.query.get(good_id)
        if theGood.icon != None:
            # 删除该商品的图片
            file_path = app.config['UPLOAD_FOLDER'] + '/' + theGood.icon
            if(os.path.exists(file_path)):
                os.remove(file_path)

        db.session.delete(theGood)
        db.session.delete(theCat)
        db.session.commit()
        return True



def catHaveChildren(catId):
    children = Category.query.filter_by(parent=catId).first()
    if children == None:
        return False
    else:
        return True


def deleteCat(catId):
    theCat = Category.query.get(catId)
    if theCat == None:
        return False
    else:
        db.session.delete(theCat)
        db.session.commit()
        return True


def searchNextCatId(catId):
    cats = Category.query.filter_by(parent=catId).all()
    catsIdList = []
    for cat in cats:
        catsIdList.append(cat.id)
    return catsIdList


def theCatFixProfit(catId):
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

    theCat = Category.query.get(catId)

    return dict(id=theCat.id, name=theCat.name, parent=theCat.parent, level=theCat.level, 
                day_profit=day_profit, month_profit=month_profit, year_profit=year_profit)


def goodIdToName(good_id):
    return Good.query.get(good_id).name


def topCats():
    cats = to_json(Category.query.filter_by(parent=0).all())
    return cats

