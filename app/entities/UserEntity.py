'''
Author: yykzjh
Date: 2021-01-04 09:06:11
Description: 用户实体的方法接口
'''

from sqlalchemy import (or_, func)
from app.models import db, User

'''
Description: 查询用户是否存在
Author: yykzjh
Date: 2021-01-04 09:48:56
Param: 
Return: 
param {账号:str} id
param {密码:int} password
'''
def select(id, password):
    user = User.query.filter_by(id=id, password=password).first()
    if user == None:
        return False
    else:
        return True
