import os
from dotenv import load_dotenv
import dash
from dash import dcc, html
import plotly.express as px
from database import SessionLocal
from models import User, Order
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Fetch the SECRET_KEY from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

if SECRET_KEY is None:
    raise ValueError("No SECRET_KEY found in environment variables")

# Initialize Dash app
app = dash.Dash(__name__)

# Set the secret key for the app (needed for session management)
app.secret_key = SECRET_KEY


# Helper function to query the database for users and their orders
def get_user_orders():
    with SessionLocal() as session:
        # Query users and their corresponding orders
        orders = session.query(Order.user_id, User.username, User.email, Order.id).join(User).all()
        return orders


# Convert query results to DataFrame for Dash
def orders_to_df(orders):
    # Group by User and count the number of orders for each user
    data = pd.DataFrame(orders, columns=["User ID", "Name", "Email", "Order ID"])
    user_order_count = data.groupby(["User ID", "Name"]).size().reset_index(name="Order Count")
    return user_order_count


# Layout of the Dash app
app.layout = html.Div([
    html.H1("Wild Rift Orders Dashboard"),

    # Data table to display the orders chart
    html.Div(id="table-container")
])


# Function to create the orders chart
def update_table():
    # Get user orders data and convert it to a DataFrame
    orders = get_user_orders()
    df = orders_to_df(orders)

    # Create a bar chart showing the number of orders for each user
    return html.Div([
        dcc.Graph(figure=px.bar(df, x="Name", y="Order Count", title="Orders per User"))  # Bar chart for orders by user
    ])


# Directly set the table-container to update the chart without callbacks
app.layout.children.append(update_table())

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
