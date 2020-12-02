from API import engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData

Base = declarative_base()


class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    userID = Column(Integer)
    shipDate = Column(String(64))
    #test = Column(String(64))
    complete = Column(Boolean)
    bought_products = relationship('Product', backref='purchase_owner')
    status = Column(String(32))


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    status = Column(String(32))
    amount = Column(Integer)
    is_bought = Column(Boolean)
    purchase_id = Column(Integer, ForeignKey('purchase.id'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    email = Column(String(32))
    password = Column(String(32))
    user_status = Column(String(32))
    bought_products = relationship('Product', backref='purchase_owner')
    status = Column(String(32))


class ProductList(Base):
    __tablename__ = 'product_list'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    all_products = relationship('Product', backref='purchase_owner')

# Base.metadata.create_all(engine)
