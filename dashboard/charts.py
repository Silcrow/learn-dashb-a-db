import plotly.express as px
from dash import dcc, html
from .queries import get_order_costs, orders_to_df


def create_order_chart():
    """Generate bar chart for total order costs."""
    orders = get_order_costs()
    df = orders_to_df(orders)
    return html.Div([
        dcc.Graph(figure=px.bar(df, x="Order ID", y="Total Cost", title="Total Order Costs"))
    ])
