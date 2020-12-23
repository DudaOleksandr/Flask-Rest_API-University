from flask_bcrypt import check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from API import session

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    status = Column(String(32))
    amount = Column(Integer)
    is_bought = Column(Boolean)
    purchased = relationship('Purchase', backref='product')


class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    userID = Column(Integer)
    shipDate = Column(String(64))
    complete = Column(Boolean)
    product_id = Column(Integer, ForeignKey('product.id'))
    product_r = relationship(Product, foreign_keys=[product_id])

    status = Column(String(32))


class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    status = fields.Str()
    amount = fields.Int()
    is_bought = fields.Bool()
    purchased = relationship('Purchase', backref='product')

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)


class PurchaseSchema(Schema):
    id = fields.Int()
    quantity = fields.Int()
    userID = fields.Int()
    shipDate = fields.Str()
    complete = fields.Bool()
    status = fields.Str()
    product_id = Column(Integer, ForeignKey('product.id'))
    product_r = fields.Nested(ProductSchema)

    @post_load
    def make_purchase(self, data, **kwargs):
        return Purchase(**data)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    email = Column(String(32))
    password = Column(String(64))
    user_status = Column(String(32))
    status = Column(String(32))

    def check_password(self, secret):
        return check_password_hash(self.password, secret)


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


def check_None(cls, pk):
    obj = session.query(cls).get(pk)
    if obj is None:
        raise Exception
    return obj
