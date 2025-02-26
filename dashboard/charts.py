import plotly.express as px
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash import html

from .queries import get_order_costs, get_users_with_orders, get_total_revenue, get_total_orders, get_bestselling_products


def create_order_chart():
    """Generate bar chart for total order costs."""
    df = get_order_costs()
    return html.Div([
        dcc.Graph(figure=px.bar(df, x="Order ID", y="Total Cost", title="Total Order Costs"))
    ])


def generate_table(dataframe, max_rows=10):
    """Generate HTML table from DF."""
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def generate_collapsible_table():
    df = get_users_with_orders()

    return dash_table.DataTable(
        id="orders-table",
        columns=[
            {"name": "User ID", "id": "User ID"},
            {"name": "Username", "id": "Username"},
            {"name": "Order ID", "id": "Order ID"},
            {"name": "Order Date", "id": "Order Date"},
            {"name": "Product", "id": "Product"},
            {"name": "Quantity", "id": "Quantity"},
            {"name": "Price", "id": "Price"},
        ],
        data=df.to_dict("records"),
        style_table={"overflowX": "auto"},
        row_selectable="multi",
        filter_action="native",
        sort_action="native",
        page_size=10
    )


def generate_total_revenue_card():
    """Generate a KPI card displaying total revenue."""
    total_revenue = get_total_revenue()
    return dbc.Card([
        dbc.CardBody([
            html.H4("Total Revenue", className="card-title"),
            html.H2(f"${total_revenue:,.2f}", className="card-text text-success"),
        ])
    ], className="shadow-sm p-3 mb-4 bg-white rounded")


def generate_total_orders_card():
    """Generate a KPI card displaying total orders."""
    total_orders = get_total_orders()
    return dbc.Card([
        dbc.CardBody([
            html.H4("Total Orders", className="card-title"),
            html.H2(f"{total_orders:,}", className="card-text text-primary"),
        ])
    ], className="shadow-sm p-3 mb-4 bg-white rounded")


def generate_bestselling_products_chart():
    fig = px.bar(
        get_bestselling_products(),
        x="Product Name",
        y="Total Sold",
        title="Bestsellers",
        text_auto=True
    )
    fig.update_layout(xaxis_tickangle=-45)  # Rotate x-axis labels for readability
    return dcc.Graph(figure=fig)
