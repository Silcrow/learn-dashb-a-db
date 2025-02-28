from sqlalchemy import func
import pandas as pd
from sqlalchemy.orm import joinedload
from database.database import SessionLocal
from database.models import Order, OrderItem, User, Product


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


def get_total_revenue():
    """Calculate the total revenue from all orders."""
    with SessionLocal() as session:
        total_revenue = session.query(OrderItem.price).all()
        return sum([item[0] for item in total_revenue])


def get_total_orders():
    """Get the total number of orders."""
    with SessionLocal() as session:
        total_orders = session.query(Order.id).count()
        return total_orders


def get_bestselling_products():
    """Query database to get bestselling products."""
    with SessionLocal() as session:
        bestselling_products = (
            session.query(
                Product.name,
                func.sum(OrderItem.quantity).label("total_sold")
            )
            .join(OrderItem, Product.id == OrderItem.product_id)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())  # Sort from highest sales
            .all()
        )
    return pd.DataFrame(bestselling_products, columns=["Product Name", "Total Sold"])


def get_total_customers():
    """Query the database to get the total number of customers."""
    with SessionLocal() as session:
        total_customers = session.query(User).count()  # Assuming User is the table with customer data
    return total_customers


def get_total_spent_by_customers():
    """Query the database to get total money spent by each customer."""
    with SessionLocal() as session:
        total_spent_by_customers = (
            session.query(
                User.username,  # Assuming 'name' is the customer's name
                func.sum(OrderItem.price * OrderItem.quantity).label("total_spent")
            )
            .join(Order, Order.user_id == User.id)  # Assuming Order has 'user_id'
            .join(OrderItem, Order.id == OrderItem.order_id)  # Assuming OrderItem is linked to Order
            .group_by(User.id, User.username)  # Group by user to get total spent per customer
            .order_by(func.sum(OrderItem.price * OrderItem.quantity).desc())  # Sort from highest spender
            .all()
        )
    return pd.DataFrame(total_spent_by_customers, columns=["Customer Name", "Total Spent"])
# TODO: feels like the sessions in each function can be encapsulated
