import plotly.express as px
from dash import dcc, html
from .queries import get_order_costs, get_usernames


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


def generate_users_table():
    return generate_table(get_usernames())
