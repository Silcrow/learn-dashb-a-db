from sqlalchemy.orm import Session
from .models import User, Product, Order, OrderItem


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
def create_product(session: Session, name: str, price: float, description: str, stock_quantity: int) -> Product:
    product = Product(name=name, price=price, description=description, stock_quantity=stock_quantity)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def get_product_by_id(session: Session, product_id: int) -> Product:
    return session.query(Product).filter(Product.id == product_id).first()


def get_products_by_user(session: Session, user_id: int) -> list:
    # Here we fetch products based on orders of the user, not directly linked to users
    orders = session.query(Order).filter(Order.user_id == user_id).all()
    product_ids = set(item.product_id for order in orders for item in order.order_items)
    return session.query(Product).filter(Product.id.in_(product_ids)).all()


# Order CRUD operations
def create_order(session: Session, user_id: int) -> Order:
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order_by_id(session: Session, order_id: int) -> Order:
    return session.query(Order).filter(Order.id == order_id).first()


def get_orders_by_user(session: Session, user_id: int) -> list:
    return session.query(Order).filter(Order.user_id == user_id).all()


# OrderItem CRUD operations
def create_order_item(session: Session, order_id: int, product_id: int, quantity: int, price: float) -> OrderItem:
    order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price)
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item


def get_order_items_by_order(session: Session, order_id: int) -> list:
    return session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
