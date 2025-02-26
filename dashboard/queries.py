from sqlalchemy import func
import pandas as pd
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


def get_usernames():
    """Query database to get all usernames as DF."""
    with SessionLocal() as session:
        users = session.query(
            User.id, User.username
        ).all()
    return pd.DataFrame(users, columns=["User ID", "Username"])
