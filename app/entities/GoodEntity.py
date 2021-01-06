'''
Author: yykzjh
Date: 2021-01-04 09:03:32
Description: 商品实体的方法接口
'''
from sqlalchemy import (or_, func, not_, and_ ) 
from app.models import db, Category, to_json


'''
description: 返回指定分类下的所有商品id
author: yykzjh
Date: 2021-01-06 10:15:40
param {分类id:int} cat_id
return {该分类下所有商品id:[int]}
'''
def searchGoodsId(cat_id):
    allGoodsId = []
    allCatId = [cat_id]

    while True:
        preAllCatId = []
        print(allCatId)
        for catId in allCatId:
            lowCatId = Category.query.with_entities(Category.id).filter(and_(Category.parent==catId, not_(Category.level==4))).all()
            lowCatId = [turple[0] for turple in lowCatId]
            preAllCatId.extend(lowCatId)
            lowGoodsId = Category.query.with_entities(Category.id).filter(and_(Category.parent==catId, Category.level==4)).all()
            lowGoodsId = [turple[0] for turple in lowGoodsId]
            allGoodsId.extend(lowGoodsId)
            print(allGoodsId)
        if preAllCatId:
            allCatId = preAllCatId
        else:
            break
    print(allGoodsId)
    return allGoodsId

