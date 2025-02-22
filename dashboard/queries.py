from sqlalchemy import func
import pandas as pd
from database.database import SessionLocal
from database.models import Order, OrderItem


def get_order_costs():
    """Query database to get total cost per order."""
    with SessionLocal() as session:
        results = session.query(
            Order.id,
            func.sum(OrderItem.quantity * OrderItem.price).label('total_cost')
        ).join(OrderItem).group_by(Order.id).all()
    return results


def orders_to_df(orders):
    """Convert order query results to a pandas DataFrame."""
    return pd.DataFrame(orders, columns=["Order ID", "Total Cost"])
