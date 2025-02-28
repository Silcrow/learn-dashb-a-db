import plotly.express as px
from dash import dcc, dash_table
import dash_bootstrap_components as dbc
from dash import html


def generate_collapsible_table(df):
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


def generate_total_revenue_card(total_revenue):
    """Generate a KPI card displaying total revenue."""
    return dbc.Card([
        dbc.CardBody([
            html.H4("Total Revenue", className="card-title"),
            html.H2(f"${total_revenue:,.2f}", className="card-text text-success"),
        ])
    ], className="shadow-sm p-3 mb-4 bg-white rounded")


def generate_total_orders_card(total_orders):
    """Generate a KPI card displaying total orders."""
    return dbc.Card([
        dbc.CardBody([
            html.H4("Total Orders", className="card-title"),
            html.H2(f"{total_orders:,}", className="card-text text-primary"),
        ])
    ], className="shadow-sm p-3 mb-4 bg-white rounded")


def generate_bestselling_products_chart(bestselling_products):
    """Generate a bestsellers bar chart from df."""
    fig = px.bar(
        bestselling_products,
        x="Product Name",
        y="Total Sold",
        title="Bestseller Products",
        text_auto=True
    )
    fig.update_layout(xaxis_tickangle=-45)  # Rotate x-axis labels for readability
    return dcc.Graph(figure=fig)


def generate_total_customers_card(total_customers):
    """Generate a KPI card displaying total customers."""
    return dbc.Card([
        dbc.CardBody([
            html.H4("Total Customers", className="card-title"),
            html.H2(f"{total_customers}", className="card-text text-info"),
        ])
    ], className="shadow-sm p-3 mb-4 bg-white rounded")


def generate_total_spent_by_customers_chart(df):
    """Generate a bar chart of total money spent by each customer."""
    fig = px.bar(
        df,
        x="Customer Name",  # x-axis for customer names
        y="Total Spent",  # y-axis for the total amount spent
        title="Whales (Top Spenders)",
        text_auto=True  # Show values on the bars
    )
    fig.update_layout(
        xaxis_tickangle=-45,  # Rotate x-axis labels for readability
        yaxis_title="Total Money Spent ($)",
        xaxis_title="Customer Name"
    )
    return dcc.Graph(figure=fig)
