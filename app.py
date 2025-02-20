from models import SessionLocal, User, Product, Order


def create_data():
    # Create a new session
    session = SessionLocal()

    # Insert a new user
    new_user = User(username="john_doe", email="john@example.com")
    session.add(new_user)
    session.commit()

    # Insert a new product for the user
    new_product = Product(name="Laptop", price=1000, owner=new_user)
    session.add(new_product)
    session.commit()

    # Insert an order for the user
    new_order = Order(order_date="2025-02-21", total_price=1200, user=new_user)
    session.add(new_order)
    session.commit()

    print("Data inserted successfully!")

    # Close the session
    session.close()


if __name__ == "__main__":
    create_data()
