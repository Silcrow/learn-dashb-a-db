import os
from dotenv import load_dotenv
import dash
from dash import dcc, html
import plotly.express as px
from sqlalchemy import func
from database import SessionLocal
from models import User, Order, OrderItem
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


# Helper function to query the database for total order costs
def get_order_costs():
    with SessionLocal() as session:
        # Query the total cost per order (sum of quantity * price for each item)
        results = session.query(
            Order.id,  # Order ID
            func.sum(OrderItem.quantity * OrderItem.price).label('total_cost')  # Sum the cost of each item in the order
        ).join(OrderItem).group_by(Order.id).all()  # Join with OrderItem and group by Order ID
        return results


# Convert query results to DataFrame for Dash
def orders_to_df(orders):
    # Convert the results to a DataFrame
    data = pd.DataFrame(orders, columns=["Order ID", "Total Cost"])
    return data


# Layout of the Dash app
app.layout = html.Div([
    html.H1("Wild Rift Orders Dashboard"),

    # Data table to display the orders chart
    html.Div(id="table-container")
])


# Function to create the orders chart
def update_table():
    # Get the total costs of orders
    orders = get_order_costs()
    df = orders_to_df(orders)

    # Create a bar chart showing the total cost for each order
    return html.Div([
        dcc.Graph(figure=px.bar(df, x="Order ID", y="Total Cost", title="Total Order Costs"))  # Bar chart for total order cost
    ])


# Directly set the table-container to update the chart without callbacks
app.layout.children.append(update_table())

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
