import os
from dotenv import load_dotenv
import dash
from dash import html
import dash_bootstrap_components as dbc
from .charts import generate_collapsible_table, generate_total_revenue_card, \
    generate_total_orders_card, generate_bestselling_products_chart, generate_total_customers_card, \
    generate_total_spent_by_customers_chart
from .queries import get_bestselling_products, get_total_orders, get_total_revenue, get_users_with_orders, \
    get_total_customers, get_total_spent_by_customers

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("No SECRET_KEY found in environment variables")

# Initialize Dash app
app = dash.Dash(__name__)
app.secret_key = SECRET_KEY

# Layout
app.layout = html.Div([
    html.H1("Wild Rift Orders Dashboard"),

    # KPI Cards - Total Revenue, Total Orders, Total Customers
    dbc.Container([
        dbc.Row([
            dbc.Col(generate_total_revenue_card(get_total_orders())),
            dbc.Col(generate_total_orders_card(get_total_revenue())),
            dbc.Col(generate_total_customers_card(get_total_customers()))
        ])
    ]),

    # Add the "Bestselling Products" Chart
    html.Div(id="table-container", children=generate_bestselling_products_chart(get_bestselling_products())),

    # Add the "Total Money Spent by Customers" Chart
    html.Div(id="total-spent-chart-container", children=generate_total_spent_by_customers_chart(
        get_total_spent_by_customers())),

    # Orders Overview Section
    dbc.Container([
        html.H3("Orders Overview"),
        generate_collapsible_table(get_users_with_orders()),
    ]),
])

