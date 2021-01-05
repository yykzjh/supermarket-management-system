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
    if user == None:
        return False
    else:
        return True


def detail(id):
    user = User.query.filter_by(id=id).first()
    return user


def details(role_name):
    users = Role.query.filter_by(name=role_name).first().users.all()
    return users


# if __name__ == "__main__":
#     # print(detail(2017040394))
#     # print(details(("staff"))[0].password)
#     # print(details(("superadmin"))[0].password)