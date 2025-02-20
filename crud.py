# crud.py
from models import User, Product, Order
from sqlalchemy.orm import Session


# User CRUD operations
def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User:
    return session.query(User).filter(User.id == user_id).first()


def get_all_users(session: Session) -> list:
    return session.query(User).all()


# Product CRUD operations
def create_product(session: Session, name: str, price: int, user_id: int) -> Product:
    product = Product(name=name, price=price, user_id=user_id)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def get_product_by_id(session: Session, product_id: int) -> Product:
    return session.query(Product).filter(Product.id == product_id).first()


def get_products_by_user(session: Session, user_id: int) -> list:
    return session.query(Product).filter(Product.user_id == user_id).all()


# Order CRUD operations
def create_order(session: Session, order_date: str, total_price: int, user_id: int) -> Order:
    order = Order(order_date=order_date, total_price=total_price, user_id=user_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order_by_id(session: Session, order_id: int) -> Order:
    return session.query(Order).filter(Order.id == order_id).first()


def get_orders_by_user(session: Session, user_id: int) -> list:
    return session.query(Order).filter(Order.user_id == user_id).all()


# crud.py
def fetch_sample_data(session: Session, limit: int = 5):
    # Fetch a limited number of users
    users = session.query(User).limit(limit).all()
    print("Users:")
    for user in users:
        print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")

    # Fetch a limited number of products for the first user (if exists)
    if users:
        first_user = users[0]
        products = session.query(Product).filter(Product.user_id == first_user.id).limit(limit).all()
        print(f"\nProducts of user {first_user.username}:")
        for product in products:
            print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}")

    # Fetch a limited number of orders for the first user (if exists)
    if users:
        first_user = users[0]
        orders = session.query(Order).filter(Order.user_id == first_user.id).limit(limit).all()
        print(f"\nOrders of user {first_user.username}:")
        for order in orders:
            print(f"Order ID: {order.id}, Date: {order.order_date}, Total Price: {order.total_price}")
