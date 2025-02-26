import os
from dotenv import load_dotenv
import dash
from dash import html
import dash_bootstrap_components as dbc
from .charts import create_order_chart, generate_collapsible_table

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
    html.Div(id="table-container", children=create_order_chart()),
    dbc.Container([
            html.H3("Orders Overview"),
            generate_collapsible_table(),
        ]),
])
