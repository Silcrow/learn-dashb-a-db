import os
from dotenv import load_dotenv
import dash
from dash import html, dcc
from .charts import create_order_chart

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
    html.Div(id="table-container", children=create_order_chart())  # Calls chart function
])

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
