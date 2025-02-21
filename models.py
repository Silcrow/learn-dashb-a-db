# models.py
import pendulum

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, validates
from database import Base


class User(Base):
    """The customer who places the orders."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, default=lambda: pendulum.now("UTC"))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @property
    def total_price(self):
        # Calculate the total price dynamically from related OrderItems
        return sum(item.price for item in self.order_items)

    @total_price.setter
    def total_price(self, value):
        # This will be ignored because we automatically calculate it
        pass


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=1)
    price = Column(Float)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    stock_quantity = Column(Integer, default=0)
    order_items = relationship("OrderItem", back_populates="product")
