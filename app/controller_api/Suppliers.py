from flask import Blueprint, request, jsonify, session
from app.entities.SupplierEntity import (details, addSupplier, deleteSupplier, updateSupplier,
    divideProvince, divideCity )


app_suppliers = Blueprint("app_suppliers", __name__)



@app_suppliers.route("/Index")
def index():
    return "suppliers index"


'''
description: 返回所有供应商信息
author: yykzjh
Date: 2021-01-05 21:20:10
param {无}
return JSON {StatusCode:200/400, suppliers:[Supplier]}
'''
@app_suppliers.route("/SuppliersInfo", methods=["GET"])
def allSuppliers():
    suppliers = details()

    if suppliers == None:
        return jsonify(StatusCode=400)
    else:
        return jsonify(StatusCode=400, suppliers=suppliers)


'''
description: 新增供应商
author: yykzjh
Date: 2021-01-08 15:14:45
param {供应商名称:str} name
param {供应商电话:str} mobile
param {供应商所在省:str} province
param {供应商所在市:str} city
param {签约起始时间:datetime} sign_start
param {签约到期时间:datetime} sign_end
return JSON {StatusCode:200/400, msg:"同样的位置已有同名供应商！"}
'''
@app_suppliers.route("/NewSupplier", methods=["POST"])
def insertSupplier():
    supplier_info = request.get_json()
    name = supplier_info.get('name')
    mobile = supplier_info.get('mobile')
    province = supplier_info.get('province')
    city = supplier_info.get("city")
    sign_start = supplier_info.get('sign_start')
    sign_end = supplier_info.get('sign_end')

    if addSupplier(name,mobile,province,city,sign_start, sign_end):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400, msg="同样的位置已有同名供应商！")


'''
description: 删除指定id的供应商 、
author: yykzjh
Date: 2021-01-08 15:20:06
param {供应商id:int} id
return {StatusCode:200/400, msg:"没有该供应商"}
'''
@app_suppliers.route("/DeleteSupplier", methods=["GET"])
def delete():
    supplier_id = request.args.get('id')
    if deleteSupplier(supplier_id):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400, msg="没有该供应商！")


'''
description: 更新指定供应商信息
author: yykzjh
Date: 2021-01-08 15:29:25
param {供应商id:int} id
param {供应商名称:str} name
param {供应商电话:str} mobile
param {供应商所在省:str} province
param {供应商所在市:str} city
param {签约起始时间:datetime} sign_start
param {签约到期时间:datetime} sign_end
return {StatusCode:200/400, msg:"没有该供应商"}
'''
@app_suppliers.route("/ModifySupplier", methods=["POST"])
def update():
    supplier_info = request.get_json()
    id = supplier_info.get("id")
    name = supplier_info.get('name')
    mobile = supplier_info.get('mobile')
    province = supplier_info.get('province')
    city = supplier_info.get("city")
    sign_start = supplier_info.get('sign_start')
    sign_end = supplier_info.get('sign_end')

    if updateSupplier(id, name=name, mobile=mobile, province=province, city=city, \
                sign_start=sign_start, sign_end = sign_end):
        return jsonify(StatusCode=200)
    else:
        return jsonify(StatusCode=400, msg="没有该供应商！")


'''
description: 返回各省市供应商数量的统计信息
author: yykzjh
Date: 2021-01-08 16:19:02
param {无}
return {data:{中国:[dict],其他省:[dict]}} dict:{name,value}
'''
@app_suppliers.route("/StatisticInfo", methods=["GET"])
def statisticInformation():
    data = dict()
    data["中国"] = divideProvince()
    for province in data["中国"]:
        data[province['name']] = divideCity(province['name'])

    return jsonify(data=data)