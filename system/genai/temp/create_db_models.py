# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime

logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


class Customer(Base):
    """description: Table storing customer details, each customer can have multiple orders."""
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    credit_limit = Column(Float, nullable=False)
    balance = Column(Float, nullable=False, default=0.0)


class Order(Base):
    """description: Table storing orders placed by customers, each order can have multiple items."""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(Date, nullable=False)
    amount_total = Column(Float, nullable=False, default=0.0)


class Item(Base):
    """description: Table storing items in orders."""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False, default=0.0)


class Product(Base):
    """description: Table storing product details specifically for men's golf shoes."""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)


# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

# Sample test data for Shopping Cart application

# Customers
customer1 = Customer(id=1, name='John Doe', email='john.doe@example.com', credit_limit=1000.0, balance=0.0)
customer2 = Customer(id=2, name='Jane Smith', email='jane.smith@example.com', credit_limit=1500.0, balance=0.0)

# Products
product1 = Product(id=1, name="Nike Air", unit_price=150.0)
product2 = Product(id=2, name="Adidas Boost", unit_price=120.0)

# Orders
order1 = Order(id=1, customer_id=1, order_date=date(2023, 10, 1), amount_total=0.0)
order2 = Order(id=2, customer_id=2, order_date=date(2023, 10, 2), amount_total=0.0)

# Items
item1 = Item(id=1, order_id=1, product_id=1, quantity=2, unit_price=150.0, amount=0.0)
item2 = Item(id=2, order_id=1, product_id=2, quantity=1, unit_price=120.0, amount=0.0)
item3 = Item(id=3, order_id=2, product_id=1, quantity=3, unit_price=150.0, amount=0.0)


session.add_all([customer1, customer2, product1, product2, order1, order2, item1, item2, item3])
session.commit()
