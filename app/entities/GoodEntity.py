'''
Author: yykzjh
Date: 2021-01-04 09:03:32
Description: 商品实体的方法接口
'''
from sqlalchemy import (or_, func, not_, and_ ) 
from app.models import db, Category, to_json, Good


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
def goodDetails(good_id):
    good = Good.query.get(good_id).to_dict()
    return good