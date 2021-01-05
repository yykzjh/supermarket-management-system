'''
Author: yykzjh
Date: 2021-01-04 09:06:11
Description: 用户实体的方法接口
'''

from sqlalchemy import (or_, func)
# import sys
# sys.path.append("..")
from app.models import db, User, Role

'''
Description: 查询用户是否存在
Author: yykzjh
Date: 2021-01-04 09:48:56
param {账号:str} id
param {密码:int} password
'''
def select(id, password):
    user = User.query.filter_by(id=id, password=password).first()
    return user

'''
description: 返回指定用户的信息
author: yykzjh
Date: 2021-01-05 17:40:20
param {账号:str} id
return {user:User}
'''
def detail(id):
    user = User.query.filter_by(id=id).first()
    return user

'''
description: 返回指定角色的所有用户信息
author: yykzjh
Date: 2021-01-05 17:40:56
param {角色名:str} role_name
return {users:[User]}
'''
def details(role_name):
    users = Role.query.filter_by(name=role_name).first().users.all()
    return users


'''
description: 修改指定用户的密码或者权限
author: yykzjh
Date: 2021-01-05 17:57:49
param {账号:str} id
param {密码:str} password
param {角色id:int} role_id
return {True/False}
'''
def update(id, password = None, role_id = None):
    user = User.query.filter_by(id=id).first()
    if user == None:
        return False
    else:
        if password != None:
            user.password = password
        if role_id != None:
            user.role_id = role_id
        db.session.commit()
        return True




# if __name__ == "__main__":
#     # print(detail(2017040394))
#     # print(details(("staff"))[0].password)
#     # print(details(("superadmin"))[0].password)