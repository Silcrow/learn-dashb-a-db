import plotly.express as px
import plotly.graph_objects as go
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


def generate_kpi_card(title, value):
    """Generate a KPI card displaying title and value."""
    return dbc.Card([
        dbc.CardBody([
            html.H4(f"{title}", className="card-title"),
            html.H2(f"${value}", className="card-text text-success"),
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


def generate_split_bar(value, total):
    """Generates a split bar showing the high-spending vs other customers."""
    # Calculate the percentage
    high_spending_percentage = value / total
    others_percentage = 1 - high_spending_percentage

    # Create a simple horizontal bar with two colored sections
    return html.Div(
        children=[
            # High-spending section
            html.Div(
                children=[
                    html.Span(f"{value} Whales", style={'fontWeight': 'bold'}),
                ],
                style={
                    'height': '100%',  # Make it fill the full height of the container
                    'width': f'{high_spending_percentage * 100}%',  # Width based on the value
                    'backgroundColor': '#1f77b4',  # Blue color for high-spending
                    'color': 'white',
                    'display': 'inline-block',
                    'textAlign': 'center',
                    'lineHeight': '30px',
                    'fontWeight': 'bold',
                    'textOverflow': 'ellipsis',
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                }
            ),

            # "Other" customers section
            html.Div(
                children=[
                    html.Span(f"{total - value} Others", style={'fontWeight': 'bold'}),
                ],
                style={
                    'height': '100%',  # Make it fill the full height of the container
                    'width': f'{others_percentage * 100}%',  # Width based on the remaining value
                    'backgroundColor': '#d3d3d3',  # Light gray for others
                    'color': 'black',
                    'display': 'inline-block',
                    'textAlign': 'center',
                    'lineHeight': '30px',
                    'fontWeight': 'bold',
                    'textOverflow': 'ellipsis',
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                }
            ),
        ],
        style={'width': '100%', 'height': '100%', 'display': 'flex'}  # Full height, flex layout for bar
    )


def generate_total_customers_card(total_customers, high_spending_customers):
    """Generate a KPI card displaying total customers with a tree map beside it."""
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    children=[
                        # Total Customers on the left
                        html.Div(
                            children=[
                                html.H4("Total Cus", className="card-title"),
                                html.H2(f"{total_customers}", className="card-text text-primary"),
                            ],
                            style={'flex': '1', 'textAlign': 'left', 'display': 'flex', 'flexDirection': 'column',
                                   'alignItems': 'flex-start'}
                        ),

                        # Tree map bar on the right side
                        html.Div(
                            children=[generate_split_bar(high_spending_customers, total_customers)],  # The bar itself
                            style={'flex': '2', 'display': 'flex', 'marginTop': '20px'}  # Move down to align with number
                        ),
                    ],
                    style={'display': 'flex', 'width': '100%'}
                ),
            ]
        ),
        className="shadow-sm p-3 mb-4 bg-white rounded"
    )


def generate_total_spent_by_customers_chart(df, filtered_df):
    """Generate a bar chart of total money spent by each customer with different colors for the top spender."""

    # Create a set of top spender customer names
    top_spender_names = set(filtered_df['Customer Name'])

    # Create a new column for color assignment based on whether the customer is a top spender
    df['Color'] = df['Customer Name'].apply(
        lambda x: '#1f77b4' if x in top_spender_names else '#d3d3d3'
    )

    # Create the bar chart
    fig = px.bar(
        df,
        x="Customer Name",  # x-axis for customer names
        y="Total Spent",  # y-axis for the total amount spent
        title="Whales (Top Spenders)",
        text_auto=True,  # Show values on the bars
        color='Color',  # Use the 'Color' column for coloring the bars
        color_discrete_map={'#1f77b4': '#1f77b4', '#d3d3d3': '#d3d3d3'}  # Assign the colors manually
    )

    fig.update_layout(
        xaxis_tickangle=-45,  # Rotate x-axis labels for readability
        yaxis_title="Total Money Spent ($)",
        xaxis_title="Customer Name",
        showlegend=False
    )

    return dcc.Graph(figure=fig)
