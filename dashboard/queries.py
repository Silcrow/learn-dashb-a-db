from sqlalchemy import func
import pandas as pd
from sqlalchemy.orm import joinedload
from database.database import SessionLocal
from database.models import Order, OrderItem, User


def get_order_costs():
    """Query database to get total cost per order as DataFrame."""
    with SessionLocal() as session:
        orders = session.query(
            Order.id,
            func.sum(OrderItem.quantity * OrderItem.price).label('total_cost')
        ).join(OrderItem).group_by(Order.id).all()
    return pd.DataFrame(orders, columns=["Order ID", "Total Cost"])


def get_users_with_orders():
    """Query database to get all users and their orders."""
    with SessionLocal() as session:
        users = session.query(User).options(
            joinedload(User.orders).joinedload(Order.order_items).joinedload(OrderItem.product)).all()

    data = []
    for user in users:
        for order in user.orders:
            for item in order.order_items:
                data.append({
                    "User ID": user.id,
                    "Username": user.username,
                    "Order ID": order.id,
                    "Order Date": order.order_date.strftime("%Y-%m-%d"),
                    "Product": item.product.name,
                    "Quantity": item.quantity,
                    "Price": item.price
                })

    return pd.DataFrame(data, columns=["User ID", "Username", "Order ID", "Order Date", "Product", "Quantity", "Price"])
