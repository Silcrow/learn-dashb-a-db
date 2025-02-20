# dao.py
from crud import (
    create_user, get_user_by_id, get_all_users,
    create_product, get_product_by_id, get_products_by_user,
    create_order, get_order_by_id, get_orders_by_user,
    fetch_sample_data
)


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
    def create_product(session, name: str, price: int, user_id: int):
        return create_product(session, name, price, user_id)

    @staticmethod
    def get_product_by_id(session, product_id: int):
        return get_product_by_id(session, product_id)

    @staticmethod
    def get_products_by_user(session, user_id: int):
        return get_products_by_user(session, user_id)


class OrderDAO:
    @staticmethod
    def create_order(session, order_date: str, total_price: int, user_id: int):
        return create_order(session, order_date, total_price, user_id)

    @staticmethod
    def get_order_by_id(session, order_id: int):
        return get_order_by_id(session, order_id)

    @staticmethod
    def get_orders_by_user(session, user_id: int):
        return get_orders_by_user(session, user_id)


class FetchDAO:
    @staticmethod
    def fetch_data(session):
        fetch_sample_data(session)
