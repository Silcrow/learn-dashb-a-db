from .crud import (
    create_user, get_user_by_id, get_all_users,
    create_product, get_product_by_id, get_products_by_user,
    create_order, get_order_by_id, get_orders_by_user,
    create_order_item, get_order_items_by_order
)
from .models import User, Product, Order


class UserDAO:
    @staticmethod
    def create_user(session, username: str, email: str):
        return create_user(session, username, email)

    @staticmethod
    def get_user_by_id(session, user_id: int):
        return get_user_by_id(session, user_id)

    @staticmethod
    def get_all_users(session):
        return get_all_users(session)


class ProductDAO:
    @staticmethod
    def create_product(session, name: str, price: float, description: str, stock_quantity: int):
        return create_product(session, name, price, description, stock_quantity)

    @staticmethod
    def get_product_by_id(session, product_id: int):
        return get_product_by_id(session, product_id)

    @staticmethod
    def get_products_by_user(session, user_id: int):
        return get_products_by_user(session, user_id)


class OrderDAO:
    @staticmethod
    def create_order(session, user_id: int):
        return create_order(session, user_id)

    @staticmethod
    def get_order_by_id(session, order_id: int):
        return get_order_by_id(session, order_id)

    @staticmethod
    def get_orders_by_user(session, user_id: int):
        return get_orders_by_user(session, user_id)


class OrderItemDAO:
    @staticmethod
    def create_order_item(session, order_id: int, product_id: int, quantity: int, price: float):
        return create_order_item(session, order_id, product_id, quantity, price)

    @staticmethod
    def get_order_items_by_order(session, order_id: int):
        return get_order_items_by_order(session, order_id)


class FetchDAO:
    @staticmethod
    def fetch_data(session):
        # Fetch a limited number of users
        users = session.query(User).limit(5).all()
        print("Users:")
        for user in users:
            print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")

        # Fetch a limited number of products for the first user (if exists)
        if users:
            first_user = users[0]
            products = session.query(Product).filter(
                Product.id.in_([item.product_id for order in first_user.orders for item in order.order_items])).limit(
                5).all()
            print(f"\nProducts of user {first_user.username}:")
            for product in products:
                print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}")

        # Fetch a limited number of orders for the first user (if exists)
        if users:
            first_user = users[0]
            orders = session.query(Order).filter(Order.user_id == first_user.id).limit(5).all()
            print(f"\nOrders of user {first_user.username}:")
            for order in orders:
                print(f"Order ID: {order.id}, Date: {order.order_date}, Total Price: {order.total_price}")
