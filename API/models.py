from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from API import session

Base = declarative_base()


class ProductList(Base):
    __tablename__ = 'product_list'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    #all_products = relationship('ProductList', backref='product')


class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    userID = Column(Integer)
    shipDate = Column(String(64))
    complete = Column(Boolean)
    bought_products = relationship('Product', backref='purchase')
    status = Column(String(32))
    #purchase_r = relationship(ProductList, foreign_keys=[id])


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    status = Column(String(32))
    amount = Column(Integer)
    is_bought = Column(Boolean)
    purchase_id = Column(Integer, ForeignKey('purchase.id'))
    purchase_r = relationship(Purchase, foreign_keys=[purchase_id])
    # purchase_k = relationship(ProductList, foreign_keys=[purchase_id])


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    email = Column(String(32))
    password = Column(String(32))
    user_status = Column(String(32))
    status = Column(String(32))


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    user_status = fields.Str()
    status = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class PurchaseSchema(Schema):
    id = fields.Int()
    quantity = fields.Int()
    userID = fields.Int()
    shipDate = fields.Str()
    complete = fields.Bool()
    bought_products = relationship('Product', backref='purchase')
    status = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Purchase(**data)


class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    status = fields.Str()
    amount = fields.Int()
    is_bought = fields.Bool()
    purchase_id = Column(Integer, ForeignKey('purchase.id'))
    purchase_r = fields.Nested(PurchaseSchema)

    # purchase_k = relationship(ProductList, foreign_keys=[purchase_id])
    @post_load
    def make_user(self, data, **kwargs):
        return Product(**data)


class ProductListSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    all_products = fields.Nested(ProductSchema)

    @post_load
    def make_user(self, data, **kwargs):
        return ProductList(**data)


class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), unique=True)


class PlaceSchema(Schema):
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make_place(self, data, **kwargs):
        return Place(**data)

def check_None(cls, pk):
    obj = session.query(cls).get(pk)
    if obj is None:
        raise Exception
    return obj
