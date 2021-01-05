from app.config import app
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime

#创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class Role(db.Model):
    """用户角色/身份表"""
    __tablename__ = "sms_roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return '<Role: name=%r>' % self.name
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model):
    """用户表"""
    __tablename__ = "sms_users" # 指明数据库的表名

    id = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    birthday = db.Column(db.Date)
    mobile = db.Column(db.String(64))
    area = db.Column(db.String(256))
    salary = db.Column(db.Float)
    role_id = db.Column(db.Integer, db.ForeignKey("sms_roles.id"), default=1, nullable=False)

    def __repr__(self):
        return '<User: id=%r, name=%r>' % (self.id, self.name) 
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Category(db.Model):
    """商品类别表"""
    __tablename__ = "sms_cats"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    parent = db.Column(db.Integer)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Category: id=%r, name=%r, level=%r>' % (self.id, self.name, self.level)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Good(db.Model):
    """商品表"""
    __tablename__ = "sms_goods"

    id = db.Column(db.Integer, db.ForeignKey("sms_cats.id"), primary_key=True)
    intro = db.Column(db.String(256))
    icon = db.Column(db.String(128))
    category_info = db.relationship("Category")

    def __repr__(self):
        return '<Good: name=%r>' % self.category_info.name
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Supplier(db.Model):
    """供应商表"""
    __tablename__ = "sms_suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(64), nullable=False)
    province = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    sign_start = db.Column(db.Date, nullable=False)
    sign_end = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<Supplier: name=%r>' % self.name
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Purchase(db.Model):
    """进货记录"""
    __tablename__ = "sms_purchase"

    good_id = db.Column(db.Integer, db.ForeignKey("sms_goods.id"), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("sms_suppliers.id"), primary_key=True)
    buildtime = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    finishtime = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    price_in = db.Column(db.Float, nullable=False)
    if_finish = db.Column(db.Boolean, nullable=False, default=False)
    if_shelf = db.Column(db.Boolean, nullable=False, default=False)

    good_info = db.relationship('Good', backref=db.backref('purchase_orders', lazy="dynamic"))
    supplier_info = db.relationship('Supplier', backref=db.backref('purchase_orders', lazy="dynamic"))

    def __repr__(self):
        return '<Purchase: good_name=%r, supplier_name=%r, time=%r, amount=%r, price=%r, if_sale=%r>' % \
                (self.good_info.category_info.name, self.supplier_info.name, self.datetime, self.amount, self.price_in, self.if_shelf)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Sale(db.Model):
    """上架商品表"""
    __tablename__ = "sms_sales"

    good_id = db.Column(db.Integer, db.ForeignKey("sms_goods.id"), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("sms_suppliers.id"), primary_key=True)
    price_out = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    good_info = db.relationship('Good', backref=db.backref('on_sales', lazy="dynamic"))
    supplier_info = db.relationship('Supplier', backref=db.backref('on_sales', lazy="dynamic"))

    def __repr__(self):
        return '<Sale: good_name=%r, supplier_name=%r, price=%r, amount=%r>' % \
                (self.good_info.category_info.name, self.supplier_info.name, self.price_out, self.amount)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Stock(db.Model):
    """库存表"""
    __tablename__ = "sms_stocks"

    good_id = db.Column(db.Integer, db.ForeignKey("sms_goods.id"), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("sms_suppliers.id"), primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    good_info = db.relationship('Good', backref=db.backref('stocks', lazy="dynamic"))
    supplier_info = db.relationship('Supplier', backref=db.backref('stocks', lazy="dynamic"))

    def __repr__(self):
        return '<Stock: good_name=%r, supplier_name=%r, amount=%r>' % \
                (self.good_info.category_info.name, self.supplier_info.name, self.amount)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(db.Model):
    """历史订单表"""
    __tablename__ = "sms_orders"

    id = db.Column(db.BigInteger, primary_key=True)
    good_id = db.Column(db.Integer, db.ForeignKey("sms_goods.id"), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("sms_suppliers.id"), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    good_info = db.relationship('Good', backref=db.backref('history_sales', lazy="dynamic"))
    supplier_info = db.relationship('Supplier', backref=db.backref('history_sales', lazy="dynamic"))

    def __repr__(self):
        return '<Order: order_id=%r, good_name=%r, supplier_name=%r, price=%r, amount=%r>' % \
                (self.id, self.good_info.category_info.name, self.supplier_info.name, self.price, self.amount)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



def to_json(all_vendors):
    v = [ven.to_dict() for ven in all_vendors]
    return v

