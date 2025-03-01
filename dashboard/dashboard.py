import os
from dotenv import load_dotenv
import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
from .charts import generate_collapsible_table, generate_bestselling_products_chart, \
    generate_total_spent_by_customers_chart, generate_total_customers_card, generate_kpi_card
from .queries import get_bestselling_products, get_total_orders, get_total_revenue, get_users_with_orders, \
    get_total_customers, get_total_spent_by_customers, get_top_spending_customers

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("No SECRET_KEY found in environment variables")

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.secret_key = SECRET_KEY

# Layout
app.layout = html.Div([
    html.H1("Wild Rift Orders Dashboard"),

    # KPI Cards - Total Revenue, Total Orders, Total Customers
    dbc.Container([
        dbc.Row([
            dbc.Col(generate_kpi_card("Total Orders", get_total_orders())),
            dbc.Col(generate_kpi_card("Total Revenue", f"${get_total_revenue()}")),
            dbc.Col(
                # Ensure the ID for the total customers card matches the output in the callback
                html.Div(id="total-customers-card", children=generate_total_customers_card(
                    get_total_customers(), len(get_top_spending_customers())))
            ),
        ])
    ]),

    # Slider to adjust threshold
    html.Div([
        html.Label("Select Spending Threshold:"),
        dcc.Slider(
            id="threshold-slider",
            min=0, max=100, step=5,
            value=50,  # Default threshold
            marks={i: f"{i}%" for i in range(0, 110, 10)}
        ),
    ], style={"margin": "20px"}),
    # Chart Container - Updated dynamically
    html.Div(id="total-spent-chart-container", children=generate_total_spent_by_customers_chart(
        get_total_spent_by_customers(), get_top_spending_customers())),

    # Add the "Bestselling Products" Chart
    html.Div(id="table-container", children=generate_bestselling_products_chart(get_bestselling_products())),

    # Orders Overview Section
    dbc.Container([
        html.H3("Orders Overview"),
        generate_collapsible_table(get_users_with_orders()),
    ]),
])


# CALLBACK: Update the chart when the slider value changes
@app.callback(
    [
        Output("total-spent-chart-container", "children"),
        Output("total-customers-card", "children"),  # Add output for the customer card
    ],
    [Input("threshold-slider", "value")]
)
def update_content(threshold):
    # Get the top spending customers based on the threshold
    filtered_customers = get_top_spending_customers(threshold)

    # Generate the updated chart
    chart = generate_total_spent_by_customers_chart(get_total_spent_by_customers(), filtered_customers)

    # Update the total customers card with the new threshold value
    total_customers = get_total_customers()
    top_customers = len(filtered_customers)
    total_customers_card = generate_total_customers_card(total_customers, top_customers)

    return chart, total_customers_card

