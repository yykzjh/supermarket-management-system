from flask import Blueprint, request, jsonify
from app.entities.GoodEntity import searchGoodsId, categoryDetails, goodDetail, addNewCat, addNewGood
from app.models import app
import uuid
import datetime
import os
from werkzeug.utils import secure_filename


app_goods = Blueprint("app_goods", __name__)



@app_goods.route("/Index")
def index():
    return "goods index"


'''
description: 查询指定分类下所有商品id
author: yykzjh
Date: 2021-01-06 10:16:48
param {分类id:int} catId
return JSON {StatusCode:200/400, allGoods=[int]}
'''
@app_goods.route("/TheCatAllGoods", methods=["GET"])
def theCatAllGoods():
    catId = int(request.args.get('catId'))
    allGoods = searchGoodsId(catId)
    
    if len(allGoods) == 0:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=200, allGoods=allGoods)


'''
description: 返回所有商品类别详细信息的结构树
author: yykzjh
Date: 2021-01-06 16:16:08
param {无}
return {[dict]} results dict:{id, name, parent, level, children:[dict]}
'''
@app_goods.route("/AllCatDetails", methods=["GET"])
def allCatDetails():
    return jsonify(results=categoryDetails(0))


'''
description: 返回指定商品的详细信息
author: yykzjh
Date: 2021-01-07 15:16:29
param {商品id:int} good_id
return JSON {StatusCode:200/400, good:Good}
'''
@app_goods.route("/GoodDetail", methods=["GET"])
def getGoodDetail():
    good_id = request.args.get('good_id')
    good = goodDetail(good_id)
    if good == None:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=200, good=good)


'''
description: 添加一条分支的类别
author: yykzjh
Date: 2021-01-07 15:39:13
param {已知父节点的id:int} pid
param {已知父节点的层次:int} plevel
param {新添加的一条类别分支的类别名列表:[str]} name_list
return JSON {StatusCode:200/400}
'''
@app_goods.route("/NewCats", methods=["POST"])
def addNewCats():
    # 获取请求体中的数据
    info = request.get_json()
    parent_id = info.get('pid')
    parent_level = info.get('plevel')
    cats_name_list = info.get('name_list')

    # 循环添加新类别
    current_level = parent_level + 1
    for name in cats_name_list:
        parent_id = addNewCat(name, parent_id, current_level)
        # 如果添加的类别和已知类别重名，则返回错误
        if parent_id == 0:
            return jsonify(StatusCode=400)
        current_level += 1
    return jsonify(StatusCode=200)
    

'''
description: 新增商品
author: yykzjh
Date: 2021-01-07 18:01:28
param {商品名:str} name
param {商品所属类别id:int} parent
param {商品简介:str} intro
param {商品图片地址:str} picUrl
return JSON {StatusCode:200/400}
'''
@app_goods.route("/NewGood", methods=["POST"])
def insertNewGood():
    good_name = request.form.get('name')
    good_parent = request.form.get('parent')
    good_intro = request.form.get('intro')
    good_icon = request.files.get('icon')

    # 获取文件名
    icon_name = secure_filename(good_icon.filename)

    # 生成自定义图片名
    namespace = uuid.NAMESPACE_URL
    iconNewName = ''.join(str(uuid.uuid3(namespace, icon_name)).split('-')) + icon_name

    # 根据当前时间生成图片存储路径
    dateFile = datetime.datetime.now().strftime('%Y-%m-%d')
    path = dateFile + '/' + iconNewName
    adsolutePath = app.config['UPLOAD_FOLDER'] + '/' + dateFile
    
    # 保存新商品信息到数据库
    if addNewGood(good_name, good_parent, good_intro, path):
        if not os.path.exists(adsolutePath):
            os.makedirs(adsolutePath)
        good_icon.save(app.config['UPLOAD_FOLDER'] + '/' + path)
        return jsonify(StatusCode=200)
    else: 
        return jsonify(StatusCode=400)


# '''
# description: 预先上传商品图片
# author: yykzjh
# Date: 2021-01-07 21:59:18
# param {商品图片:file} icon
# return JSON {图片存储地址:str} tmp_path
# '''
# @app_goods.route("/GoodPicture", methods=["POST"])
# def uploadGoodPicture():
#     good_icon = request.files.get('icon') # 获取商品图片

#     # 获取文件名
#     icon_name = secure_filename(good_icon.filename)

#     # 生成自定义图片名
#     namespace = uuid.NAMESPACE_URL
#     iconNewName = ''.join(str(uuid.uuid3(namespace, icon_name)).split('-')) + icon_name

#     # 根据当前时间生成图片存储路径
#     dateFile = datetime.datetime.now().strftime('%Y-%m-%d')
#     path = dateFile + '/' + iconNewName
#     adsolutePath = app.config['UPLOAD_FOLDER'] + '/' + dateFile
    
#     # 保存图片到生成的目录地址
#     if not os.path.exists(adsolutePath):
#         os.makedirs(adsolutePath)
#     good_icon.save(app.config['UPLOAD_FOLDER'] + '/' + path)

#     return jsonify(tmp_path=path)