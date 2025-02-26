import plotly.express as px
from dash import dcc, html, dash_table
from .queries import get_order_costs, get_users_with_orders


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