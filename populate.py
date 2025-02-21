from sqlalchemy.orm import Session
from sqlalchemy import text
from faker import Faker
import random
from dao import UserDAO, ProductDAO, OrderDAO, OrderItemDAO  # Import your DAO classes
from database import SessionLocal
from models import User, Product, Order, OrderItem

fake = Faker()

# Wild Rift item prices (as per your initial setup)
item_prices = {
    "Weapon": {
        "Dagger": 300,
        "Long Sword": 350,
        "Pickaxe": 900,
        "Brawler's Gloves": 400,
        "Vampiric Scepter": 850,
        "BF Sword": 1300,
        "Caulfield's Warhammer": 1050,
        "Sheen": 1300,
        "Cloak of Agility": 600,
        "Executioner's Calling": 1100
    },
    "Armor": {
        "Cloth Armor": 300,
        "Chain Vest": 700,
        "Ninja Tabi": 1000,
        "Mercury's Treads": 1100,
        "Steel Shoulderguards": 1000,
        "Negatron Cloak": 1200,
        "Ruby Crystal": 500,
        "Giant's Belt": 1000,
        "Null-Magic Mantle": 800,
        "Armored Boots": 900
    },
    "Magical": {
        "Fiendish Codex": 600,
        "Blasting Wand": 860,
        "Needlessly Large Rod": 1250,
        "Hextech Revolver": 950,
        "Amplifying Tome": 435,
        "Aether Wisp": 850,
        "Forbidden Idol": 800,
        "Rejuvenation Bead": 250,
        "Vampiric Scepter": 850,
        "Luden's Echo": 3000,
        "Rylai's Crystal Scepter": 2800
    },
    "Boots": {
        "Boots of Speed": 300,
        "Berserker's Greaves": 1200,
        "Sorcerer's Shoes": 1100,
        "Ionian Boots of Lucidity": 900,
        "Boots of Swiftness": 1000,
        "Plated Steelcaps": 1100
    }
}


def populate_fake_products(session: Session):
    """Populate fake product using all products from item_prices, randomizing the stock quantity."""

    # Iterate through all products in item_prices
    for product_type, products in item_prices.items():
        for product_name, product_price in products.items():
            # Randomize the stock quantity for each product
            stock_quantity = random.randint(0, 100)  # Random quantity between 0 and 100

            # Create the product
            product = Product(
                name=product_name,
                price=product_price,
                stock_quantity=stock_quantity,
                description=f"Khajiit has {product_name} if you have coins"
            )
            session.add(product)

    session.commit()  # Commit all the products at once
    print(f"All products from {product_type} category have been added with randomized quantities.")


def create_fake_user(session: Session):
    """Create a fake user and return the user object using DAO"""
    return UserDAO.create_user(session, fake.user_name(), fake.email())


def create_fake_order(session: Session, user_id: int):
    """Create a fake order with multiple products using DAO"""
    order = OrderDAO.create_order(session, user_id)

    # Retrieve all products from the database
    products = session.query(Product).all()

    # Add random order items (1 to 5 products)
    for _ in range(random.randint(1, 5)):
        # Select a random product from the list of products
        product = random.choice(products)

        # Randomize the quantity for the order item
        quantity = random.randint(1, 3)
        price = product.price * quantity

        # Create order item
        OrderItemDAO.create_order_item(session, order.id, product.id, quantity, price)

    # Commit changes
    session.commit()

    # After creating order items, calculate the total price (if not already handled by SQLAlchemy)
    total_price = sum(item.price for item in order.order_items)  # Assuming the `order_items` relationship exists
    order.total_price = total_price
    session.commit()

    print(f"Order ID: {order.id}, Total Price: {order.total_price}")


def populate_db():
    """Populate the database with fake data using DAO"""
    # Create a session
    with SessionLocal() as session:
        # Generate fake users and their orders
        for _ in range(10):  # Creating 10 fake users
            user = create_fake_user(session)

            # Create 2 orders for each user
            for _ in range(2):
                create_fake_order(session, user.id)

        print("Database populated with users and orders (products already populated).")


def wipe_database_with_sql():
    """Delete all data using raw SQL (fast but less flexible)"""
    wipe_session = SessionLocal()

    # Execute raw SQL to truncate the tables
    wipe_session.execute(text("TRUNCATE TABLE orders, products, users CASCADE"))
    wipe_session.commit()
    print("Old data cleared with raw SQL!")

    wipe_session.close()


if __name__ == "__main__":
    # with SessionLocal() as session:
    #     populate_fake_products(session)
    populate_db()  # You can uncomment this to populate users and orders
    # wipe_database_with_sql()

