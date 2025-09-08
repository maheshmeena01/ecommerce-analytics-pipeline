import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# --- Database Connection (Corrected) ---
DB_URL = "postgresql://postgres:admin@localhost:5432/ecommerce_db"

# --- Load Data Function ---
def load_data():
    """Loads data from the sales_summary table in the database."""
    try:
        engine = create_engine(DB_URL)
        query = "SELECT sale_date, total_sales, unique_customers, total_products_sold FROM sales_summary ORDER BY sale_date"
        df = pd.read_sql(query, engine)
        df['sale_date'] = pd.to_datetime(df['sale_date'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame({
            'sale_date': [], 'total_sales': [], 'unique_customers': [], 'total_products_sold': []
        })

# --- Initialize Dash App with Bootstrap Theme ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- App Layout ---
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("E-commerce Sales Analytics Dashboard", className="text-center text-primary, mb-4"), width=12)
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-over-time-chart'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='customers-over-time-chart'), width=6),
        dbc.Col(dcc.Graph(id='products-sold-over-time-chart'), width=6)
    ]),
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,
        n_intervals=0
    )
], fluid=True)


# --- Callbacks to Update Graphs ---
@app.callback(
    [Output('sales-over-time-chart', 'figure'),
     Output('customers-over-time-chart', 'figure'),
     Output('products-sold-over-time-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    df = load_data()

    if df.empty:
        empty_fig = {'data': [], 'layout': {'title': 'No Data Available or Connection Error'}}
        return empty_fig, empty_fig, empty_fig

    sales_fig = px.line(df, x='sale_date', y='total_sales', title='Total Sales Over Time')
    customers_fig = px.bar(df, x='sale_date', y='unique_customers', title='Unique Customers per Day')
    products_fig = px.line(df, x='sale_date', y='total_products_sold', title='Products Sold Over Time')

    # CORRECTED: Escaped the backslash to remove the SyntaxWarning
    sales_fig.update_layout(xaxis_title='Date', yaxis_title='Total Sales ($)', margin=dict(l=20, r=20, t=40, b=20))
    customers_fig.update_layout(xaxis_title='Date', yaxis_title='Number of Customers', margin=dict(l=20, r=20, t=40, b=20))
    products_fig.update_layout(xaxis_title='Date', yaxis_title='Number of Products Sold', margin=dict(l=20, r=20, t=40, b=20))

    return sales_fig, customers_fig, products_fig


if __name__ == '__main__':
    app.run(debug=True)