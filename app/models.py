import datetime
from .settings import Base
from sqlalchemy import TIMESTAMP, Column, String, Integer, Float, Table, ForeignKey, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


sale_products = Table('sale_products', Base.metadata,
    Column('product_id', ForeignKey('products.product_id'), primary_key=True),
    Column('sale_id', ForeignKey('sales.sale_id'), primary_key=True),
    Column('quantity', Integer),
)

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    product_description = Column(String(255), nullable=True)
    product_price = Column(Float, nullable=False)
    category_id = Column(ForeignKey('categories.category_id'))
    inventory = relationship("Inventory", uselist=False, back_populates='product')
    sales = relationship("Sale", secondary="sale_products", back_populates='products')

class Inventory(Base):
    __tablename__ = "inventories"
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(ForeignKey('products.product_id'))
    product_quantity = Column(Integer, default=0)
    product = relationship("Product", back_populates='inventory')
    inventory_logs = relationship("InventoryLog", back_populates='inventory')

class Sale(Base):
    __tablename__ = 'sales'
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_price = Column(Float)
    sale_time = Column(TIMESTAMP(timezone=True), default=func.now())
    sale_date = Column(Date, default=func.now())
    products = relationship("Product", secondary="sale_products", back_populates='sales')

class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    inventory_id = Column(ForeignKey('inventories.inventory_id'))
    previous_quantity = Column(Integer, default=0)
    new_quantity = Column(Integer, default=1)
    updated_on = Column(DateTime, default=func.now(), onupdate=datetime.datetime.utcnow())
    inventory = relationship("Inventory", back_populates='inventory_logs')